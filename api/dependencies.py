from typing import Generator

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from config import get_settings
from db.models.user import User
from db.session import SessionLocal
from services.auth_service import decode_access_token


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> User:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or missing authorization token",
    )

    if not authorization:
        raise credentials_exception

    if not authorization.lower().startswith("bearer "):
        raise credentials_exception

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
    except JWTError as exc:
        raise credentials_exception from exc

    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise credentials_exception

    try:
        user_id = int(user_id_raw)
    except ValueError as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user
