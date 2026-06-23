from fastapi import APIRouter, WebSocket, Depends
from app.auth.service import get_user_from_token

from sqlmodel import Session
from app.core.db import get_session

from app.submissions.schemas import SubmissionRead
from app.submissions.service import get_submission_by_id
from app.submissions.exceptions import SubmissionNotFound, SubmissionForbidden

router = APIRouter()


@router.websocket("/ws/submissions/{submission_id}")
async def websocket(websocket: WebSocket,
                    submission_id: int,
                    session: Session = Depends(get_session)):
    await websocket.accept()

    websocket_user = get_user_from_token(websocket.cookies.get("token"), session)
    if websocket_user is None:
        await websocket.close(4401)
        return

    try:
        submission = get_submission_by_id(submission_id, websocket_user.id, session)
    except SubmissionNotFound:
        await websocket.close(4404)
        return
    except SubmissionForbidden:
        await websocket.close(4403)
        return

    await websocket.send_json(SubmissionRead.model_validate(submission).model_dump(mode="json"))
    await websocket.close()
    # TODO(5.7): replace single push with poll/pub-sub loop for live transitions
