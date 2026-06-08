import abc
from dataclasses import dataclass

from app.submissions.models import SubmissionStatus


@dataclass
class ExecutionResult:
    status: SubmissionStatus
    stdout: str | None = None
    stderr: str | None = None
    compile_output: str | None = None
    message: str | None = None
    runtime_ms: int | None = None
    memory_kb: int | None = None
    provider_token: str | None = None

class CodeExecutionService(abc.ABC):

    @abc.abstractmethod
    async def execute(self, code: str, language: str) -> ExecutionResult:
        """Execute the given code in the specified language and return the result as a ExecutionResult."""
        pass
