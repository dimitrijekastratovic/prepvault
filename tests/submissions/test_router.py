from app.submissions.models import SubmissionStatus
from tests.conftest import add_test_user
from tests.submissions.conftest import add_test_submission


def test_submissions_return_201_submission_created(client, submission_payload, idempotency_key):
    response = client.post(
        "/api/submissions",
        json=submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 201

    body = response.json()
    assert body["id"] > 0
    assert body["problem_id"] == submission_payload["problem_id"]
    assert body["code"] == submission_payload["code"]
    assert body["language"] == submission_payload["language"]
    assert body["status"] == SubmissionStatus.accepted.value
    assert body["stdout"] == "1\n"
    assert body["stderr"] is None
    assert body["runtime_ms"] == 5
    assert body["memory_kb"] == 1024


def test_submissions_return_401_when_client_unauthenticated(unauthenticated_client, submission_payload, idempotency_key):
    response = unauthenticated_client.post(
        "/api/submissions",
        json=submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 401


def test_submissions_return_404_when_problem_is_not_found(client, bad_submission_payload, idempotency_key):
    response = client.post(
        "/api/submissions",
        json=bad_submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 404

def test_submissions_return_200_when_submission_duplicated(client, submission_payload, idempotency_key):
    client.post(
        "/api/submissions",
        json=submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    response = client.post(
        "/api/submissions",
        json=submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 200

def test_submissions_return_200_and_original_body_when_same_key_different_submission(client, submission_payload, submission_payload2, idempotency_key):
    client.post(
        "/api/submissions",
        json=submission_payload,
        headers={"Idempotency-Key": idempotency_key},
    )

    response = client.post(
        "/api/submissions",
        json=submission_payload2,
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["problem_id"] == submission_payload["problem_id"]
    assert body["code"] == submission_payload["code"]
    assert body["language"] == submission_payload["language"]


def test_submissions_return_422_when_body_malformed(client, idempotency_key):
    response = client.post(
        "/api/submissions",
        json={"malformed_body":"error"},
        headers={"Idempotency-Key": idempotency_key},
    )

    assert response.status_code == 422

## Not sure if this is possible to test
#def test_submissionreturn_409_when_submission_conflict():
#    raise NotImplemented

def test_get_submission_returns_200_for_owner(client, submission_id):
    response = client.get(f"/api/submissions/{submission_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == submission_id
    assert body["status"] == "accepted"

    
def test_get_submission_returns_404_when_not_found(client, submission_id):
    response = client.get(f"/api/submissions/{submission_id + 1}")

    assert response.status_code == 404

def test_get_submission_returns_403_for_other_user(client, session, problem_id):
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

    response = client.get(f"/api/submissions/{other_submission_id}")

    assert response.status_code == 403

def test_get_submission_returns_401_when_client_unauthenticated(unauthenticated_client, submission_id):
    response = unauthenticated_client.get(f"/api/submissions/{submission_id}")

    assert response.status_code == 401
