from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assistant import AssistantQuery, AssistantResponse, ConversationSummary
from app.services.assistant import AssistantService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/query", response_model=AssistantResponse)
def query_assistant(
    payload: AssistantQuery,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> AssistantResponse:
    service = AssistantService(db, current_user)
    try:
        conversation, reply = service.run_query(
            conversation_id=payload.conversation_id,
            message=payload.message,
            confirm=payload.confirm,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return AssistantResponse(conversation_id=conversation.id, reply=reply)


@router.get("/conversations", response_model=list[ConversationSummary])
def list_conversations(current_user=Depends(get_current_user)):
    return current_user.conversations
