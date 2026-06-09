
import logging
import httpx

from app.submissions.execution.base import CodeExecutionService, ExecutionResult
from app.submissions.models import SubmissionStatus
from app.core.config import settings

logger = logging.getLogger(__name__)

def map_status(status_id: int) -> SubmissionStatus:
    match status_id:
        case 1 | 2:
            return SubmissionStatus.pending
        case 3:
            return SubmissionStatus.accepted
        case 4:
            return SubmissionStatus.wrong_answer
        case 5:
            return SubmissionStatus.time_limit_exceeded
        case 6:
            return SubmissionStatus.compile_error
        case 7 | 8 | 9 | 10 | 11 | 12:
            return SubmissionStatus.runtime_error
        case 13 | 14:
            return SubmissionStatus.internal_error
        case _:
            logger.warning(f"Unknown Judge0 status_id: {status_id}, defaulting to internal_error")
            return SubmissionStatus.internal_error
        
        
def map_language(language: str) -> int:
    match language.lower():
        case "python":
            return 71
        case "cpp":
            return 54
        case "java":
            return 62
        case "javascript":
            return 63
        case "ruby":
            return 72
        case "rust":
            return 73
        case _:
            raise ValueError(f"Unsupported language: {language}")
        
        
        
class Judge0ExecutionService(CodeExecutionService):
    def __init__(self, url: str, auth_token: str):
        self.url = url
        self.auth_token = auth_token

    async def execute(self, code: str,language: str) -> ExecutionResult:
        # new client per request to avoid connection pooling issues in tests;
        # optimize later if needed
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/submissions",
                params={"wait": "true", "base64_encoded": "false"},
                headers={"X-Auth-Token": self.auth_token},
                json={"language_id": map_language(language), "source_code": code},
            )
            response.raise_for_status()
            data = response.json()

        execution_result = ExecutionResult(
            status=map_status(data["status"]["id"]),
            stdout=data.get("stdout"),
            stderr=data.get("stderr"),
            compile_output=data.get("compile_output"),
            message=data.get("message"),
            provider_token=data.get("token"),
            runtime_ms=round(float(data.get("time")) * 1000) if data.get("time") else None,
            memory_kb=int(data.get("memory")) if data.get("memory") else None
        )
        return execution_result
    
def get_code_execution_service() -> CodeExecutionService:
    if settings.judge0_url is None or settings.judge0_url.strip() == "":
        raise ValueError("JUDGE0_URL is not set")
    if settings.judge0_auth_token == "change-me" or settings.judge0_auth_token is None or settings.judge0_auth_token.strip() == "":
        raise ValueError("JUDGE0_AUTH_TOKEN is still the placeholder default")
    return Judge0ExecutionService(
        url=settings.judge0_url,
        auth_token=settings.judge0_auth_token,
    )
        