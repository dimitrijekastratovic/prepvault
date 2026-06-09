import httpx
import pytest
import respx

from httpx import Response

from app.submissions.execution.judge0 import map_status, map_language, Judge0ExecutionService, get_code_execution_service
from app.submissions.models import SubmissionStatus
from app.core.config import settings


@pytest.mark.parametrize("status_id, expected_status", [
    (1, SubmissionStatus.pending),
    (2, SubmissionStatus.pending),
    (3, SubmissionStatus.accepted),
    (4, SubmissionStatus.wrong_answer),
    (5, SubmissionStatus.time_limit_exceeded),
    (6, SubmissionStatus.compile_error),
    (7, SubmissionStatus.runtime_error),
    (8, SubmissionStatus.runtime_error),
    (9, SubmissionStatus.runtime_error),
    (10, SubmissionStatus.runtime_error),
    (11, SubmissionStatus.runtime_error),
    (12, SubmissionStatus.runtime_error),
    (13, SubmissionStatus.internal_error),
    (14, SubmissionStatus.internal_error),
    (-1, SubmissionStatus.internal_error),
    (99, SubmissionStatus.internal_error),
])
def test_map_status_should_translate_status_ids_to_submission_statuses(status_id, expected_status):
    assert map_status(status_id) is expected_status

@pytest.mark.parametrize("language, expected_language_id", [
    ("python", 71),
    ("cpp", 54),
    ("java", 62),
    ("javascript", 63),
    ("ruby", 72),
    ("rust", 73),
    ("PYTHON", 71),  # case-insensitive
    ("Cpp", 54),
    ("Java", 62),
    ("JavaScript", 63),
    ("Ruby", 72),
    ("Rust", 73),
])
def test_map_language_should_translate_languages_to_language_ids(language, expected_language_id):
    assert map_language(language) == expected_language_id

def test_map_language_should_raise_value_error_for_unsupported_language():
    with pytest.raises(ValueError):
        map_language("unsupported-language")

def test_get_code_execution_service_should_return_judge0_execution_service(monkeypatch):
    monkeypatch.setattr(settings, "judge0_url", "https://api.com")
    monkeypatch.setattr(settings, "judge0_auth_token", "some-token")

    service = get_code_execution_service()

    assert isinstance(service, Judge0ExecutionService)
    assert service.url == "https://api.com"
    assert service.auth_token == "some-token"


@pytest.mark.parametrize("invalid_url, invalid_token", [
    ("", "some-token"),
    ("https://api.com", ""),
    (None, "some-token"),
    ("https://api.com", None),
])
def test_get_code_execution_service_with_faulty_values_should_raise_error(
    monkeypatch, invalid_url, invalid_token
):
    monkeypatch.setattr(settings, "judge0_url", invalid_url)
    monkeypatch.setattr(settings, "judge0_auth_token", invalid_token)

    with pytest.raises(ValueError):
        get_code_execution_service()


JUDGE0_URL = "http://judge0:2358"


@pytest.mark.anyio
@respx.mock
async def test_execute_should_return_execution_result_accepted():
    respx.post(f"{JUDGE0_URL}/submissions").mock(
        return_value=Response(201, json={
            "status": {"id": 3},
            "stdout": "42\n",
            "stderr": None,
            "compile_output": None,
            "message": None,
            "token": "abc-123",
            "time": "0.002",
            "memory": 3456,
        })
    )
    service = Judge0ExecutionService(JUDGE0_URL, "real-token")
    result = await service.execute(code="print(42)", language="python")

    assert result.status is SubmissionStatus.accepted
    assert result.stdout == "42\n"
    assert result.provider_token == "abc-123"
    assert result.runtime_ms == 2
    assert result.memory_kb == 3456


@pytest.mark.anyio
@respx.mock
async def test_execute_should_map_compile_error_and_pass_compile_output_through():
    respx.post(f"{JUDGE0_URL}/submissions").mock(
        return_value=Response(201, json={
            "status": {"id": 6},
            "stdout": None,
            "stderr": None,
            "compile_output": "main.cpp:1:1: error: expected ';'",
            "message": None,
            "token": "def-456",
            "time": None,
            "memory": None,
        })
    )
    service = Judge0ExecutionService(JUDGE0_URL, "real-token")
    result = await service.execute(code="int main(){}", language="cpp")

    assert result.status is SubmissionStatus.compile_error
    assert result.compile_output == "main.cpp:1:1: error: expected ';'"


@pytest.mark.anyio
@respx.mock
async def test_execute_should_leave_metrics_none_when_judge0_omits_them():
    respx.post(f"{JUDGE0_URL}/submissions").mock(
        return_value=Response(201, json={
            "status": {"id": 1},
            "stdout": None,
            "stderr": None,
            "compile_output": None,
            "message": None,
            "token": "ghi-789",
            "time": None,
            "memory": None,
        })
    )
    service = Judge0ExecutionService(JUDGE0_URL, "real-token")
    result = await service.execute(code="print(1)", language="python")

    assert result.status is SubmissionStatus.pending
    assert result.runtime_ms is None
    assert result.memory_kb is None


@pytest.mark.anyio
@respx.mock
async def test_execute_should_convert_seconds_to_milliseconds():
    respx.post(f"{JUDGE0_URL}/submissions").mock(
        return_value=Response(201, json={
            "status": {"id": 3},
            "stdout": "ok\n",
            "stderr": None,
            "compile_output": None,
            "message": None,
            "token": "jkl-012",
            "time": "1.5",
            "memory": 1024,
        })
    )
    service = Judge0ExecutionService(JUDGE0_URL, "real-token")
    result = await service.execute(code="print('ok')", language="python")

    assert result.runtime_ms == 1500
    assert result.memory_kb == 1024


@pytest.mark.anyio
@respx.mock
async def test_execute_should_propagate_error_when_judge0_returns_5xx():
    respx.post(f"{JUDGE0_URL}/submissions").mock(return_value=Response(503))
    service = Judge0ExecutionService(JUDGE0_URL, "real-token")

    with pytest.raises(httpx.HTTPStatusError):
        await service.execute(code="print(1)", language="python")