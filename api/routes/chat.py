from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from db.models.user import User
from schemas.chat import ChatRouteRequest, ChatRouteResponse, MessageRead
from services.chat_service import list_conversation_messages, route_chat

router = APIRouter()


@router.post("/route", response_model=ChatRouteResponse, status_code=status.HTTP_200_OK)
def route_prompt(
    payload: ChatRouteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatRouteResponse:
    try:
        return route_chat(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageRead])
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MessageRead]:
    return list_conversation_messages(db, current_user.id, conversation_id)
