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
