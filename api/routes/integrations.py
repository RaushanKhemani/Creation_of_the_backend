from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from db.models.user import User
from schemas.integration import APIKeyRegisterRequest
from services.integration_service import get_active_integration, register_api_key

router = APIRouter()


@router.post("/api-key")
def register_user_api_key(
    payload: APIKeyRegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    try:
        response = register_api_key(db, current_user, payload.api_key)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"success": True, "data": response.model_dump()}


@router.get("/active")
def get_active_user_integration(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    active = get_active_integration(db, current_user)
    if not active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active API key configured")
    return {"success": True, "data": active.model_dump()}
