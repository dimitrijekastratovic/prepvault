import pytest
from fastapi.websockets import WebSocketDisconnect

from app.submissions.models import SubmissionStatus
from tests.conftest import add_test_user
from tests.submissions.conftest import add_test_submission


def test_websocket_sends_submission_to_owner(client, auth_token, submission_id):
    client.cookies.set("token", auth_token)
    with client.websocket_connect(f"/api/ws/submissions/{submission_id}") as websocket:
        data = websocket.receive_json()
    
    assert data["id"] == submission_id
    assert data["status"] == "accepted"


def test_websocket_closes_4404_when_submission_not_found(client, auth_token, submission_id):
    client.cookies.set("token", auth_token)
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(f"/api/ws/submissions/{submission_id + 1}") as websocket:
            websocket.receive_json()
            
    assert exc_info.value.code == 4404


def test_websocket_closes_4403_when_submission_belongs_to_other_user(client, auth_token, session, problem_id):
    other_user_id = add_test_user(
        session,
        first_name="Other",
        last_name="User",
        email="other@example.com",
        password_hash="otherpassword123",
    )
    other_submission_id = add_test_submission(
        session,
        user_id=other_user_id,
        problem_id=problem_id,
        code="print(2)",
        language="python",
        status=SubmissionStatus.accepted,
        judge0_token="other-token",
        stdout="",
        stderr="",
        compile_output="",
        runtime_ms=0,
        memory_kb=0,
        idempotency_key="other-idempotency-key",
    )

    client.cookies.set("token", auth_token)
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(f"/api/ws/submissions/{other_submission_id}") as websocket:
            websocket.receive_json()

    assert exc_info.value.code == 4403



def test_websocket_closes_4401_when_unauthenticated(client):
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect("/api/ws/submissions/1") as websocket:
            websocket.receive_json()
            
    assert exc_info.value.code == 4401