from app.submissions.models import SubmissionStatus


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


def test_submissions_return_401_when_cookie_not_provided(unauthenticated_client, submission_payload, idempotency_key):
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