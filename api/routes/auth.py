from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from db.models.user import User
from schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from schemas.user import UserPublic
from services.auth_service import (
    authenticate_user,
    create_user,
    issue_token_pair,
    refresh_access_token,
    revoke_refresh_token,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    existing = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = create_user(db, payload)
    return {"success": True, "data": UserPublic.model_validate(user).model_dump()}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_pair = issue_token_pair(db, user)
    return {"success": True, "data": token_pair.model_dump()}


@router.post("/token")
def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_pair = issue_token_pair(db, user)
    # Keep OAuth2 token endpoint shape compatible with Swagger authorize flow.
    return token_pair.model_dump()


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> dict:
    try:
        token_pair = refresh_access_token(db, payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return {"success": True, "data": token_pair.model_dump()}


@router.post("/logout")
def logout(payload: RefreshRequest, db: Session = Depends(get_db)) -> dict:
    revoke_refresh_token(db, payload.refresh_token)
    return {"success": True, "data": {"logged_out": True}}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    return {"success": True, "data": UserPublic.model_validate(current_user).model_dump()}
