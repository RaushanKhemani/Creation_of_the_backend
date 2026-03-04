from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from typing import Callable, Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from config import get_settings
from db.models.user import User
from db.session import SessionLocal
from services.auth_service import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

_RATE_BUCKETS: dict[tuple[int, str], deque[datetime]] = defaultdict(deque)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authorization token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
    except (JWTError, ValueError) as exc:
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


def require_roles(*roles: str) -> Callable[[User], User]:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles and not current_user.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return role_checker


def enforce_rate_limit(request: Request, current_user: User = Depends(get_current_user)) -> None:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=1)
    bucket_key = (current_user.id, request.url.path)

    bucket = _RATE_BUCKETS[bucket_key]
    while bucket and bucket[0] < window_start:
        bucket.popleft()

    if len(bucket) >= settings.rate_limit_requests_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again shortly.",
        )

    bucket.append(now)
