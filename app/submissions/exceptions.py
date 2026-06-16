class SubmissionError(Exception):
    """Base class for all submission-domain errors."""


class ProblemNotFound(SubmissionError):
    """Raised when a submission references a problem that does not exist."""

    def __init__(self, problem_id: int) -> None:
        self.problem_id = problem_id
        super().__init__(f"Problem {problem_id} not found")


class SubmissionConflict(SubmissionError):
    """Raised when a submission insert hits a uniqueness collision but no
    replayable row can be found (a genuinely exceptional state)."""

class SubmissionNotFound(SubmissionError):
    """Raised when a submission references a submission id that does not exist."""

    def __init__(self, submission_id: int) -> None:
        self.submission_id = submission_id
        super().__init__(f"Submission id {submission_id} not found")

class SubmissionForbidden(SubmissionError):
    """Raised when a submission references a submission id that does not belong to the current user."""

    def __init__(self, submission_id: int) -> None:
        self.submission_id = submission_id
        super().__init__(f"Submission {submission_id} does not belong to the current user")