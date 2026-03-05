from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import enforce_rate_limit, get_current_user, get_db
from db.models.user import User
from schemas.chat import ChatRouteRequest, ChatWindowCreateRequest
from services.chat_service import create_chat_window, list_chat_messages, list_chat_windows, route_chat
from services.integration_service import normalize_provider_key

router = APIRouter()


@router.post("/windows", status_code=status.HTTP_201_CREATED)
def create_window(
    payload: ChatWindowCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    provider_key = normalize_provider_key(payload.provider_key or "chatgpt")
    return {
        "success": True,
        "data": create_chat_window(db, current_user, payload, provider_key=provider_key).model_dump(),
    }


@router.get("/windows")
def list_windows(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return {"success": True, "data": [item.model_dump() for item in list_chat_windows(db, current_user)]}


@router.post("/route", status_code=status.HTTP_200_OK)
async def route_prompt(
    payload: ChatRouteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: None = Depends(enforce_rate_limit),
) -> dict:
    try:
        response = await route_chat(db, current_user, payload)
        return {"success": True, "data": response.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/conversations/{chat_id}/messages")
def get_conversation_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return {
        "success": True,
        "data": [item.model_dump() for item in list_chat_messages(db, current_user.id, chat_id)],
    }
