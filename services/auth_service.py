from jose import jwt
from sqlalchemy.orm import Session

from config import get_settings
from core.security import create_access_token, hash_password, verify_password
from db.models.user import User
from schemas.auth import RegisterRequest, TokenResponse


def create_user(db: Session, payload: RegisterRequest, *, is_superuser: bool = False) -> User:
    user = User(
        email=payload.email.strip().lower(),
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        is_active=True,
        is_superuser=is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def issue_access_token(user: User) -> TokenResponse:
    settings = get_settings()
    token = create_access_token(
        subject=str(user.id),
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.access_token_expire_minutes,
    )
    return TokenResponse(access_token=token, expires_in_seconds=settings.access_token_expire_minutes * 60)


def decode_access_token(token: str, secret_key: str, algorithm: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=[algorithm])
