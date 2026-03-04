from datetime import datetime, timedelta, timezone
from hashlib import sha256

from jose import jwt
from sqlalchemy.orm import Session

from config import get_settings
from core.security import create_token, hash_password, verify_password
from db.models.refresh_token import RefreshToken
from db.models.user import User
from schemas.auth import RegisterRequest, TokenPair


def _hash_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def create_user(db: Session, payload: RegisterRequest, *, role: str = "user", is_superuser: bool = False) -> User:
    user = User(
        email=payload.email.strip().lower(),
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        role=role,
        is_active=True,
        is_superuser=is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def _issue_refresh_token(db: Session, user: User) -> str:
    settings = get_settings()
    expires_delta = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = create_token(
        subject=str(user.id),
        token_type="refresh",
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_delta=expires_delta,
    )
    token_hash = _hash_token(refresh_token)
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + expires_delta,
            is_revoked=False,
        )
    )
    db.commit()
    return refresh_token


def issue_token_pair(db: Session, user: User) -> TokenPair:
    settings = get_settings()
    access_token = create_token(
        subject=str(user.id),
        token_type="access",
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_token = _issue_refresh_token(db, user)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in_seconds=settings.access_token_expire_minutes * 60,
    )


def refresh_access_token(db: Session, refresh_token: str) -> TokenPair:
    settings = get_settings()
    payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    if payload.get("typ") != "refresh":
        raise ValueError("Invalid refresh token type")

    user_id = int(payload["sub"])
    token_hash = _hash_token(refresh_token)

    db_refresh = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if not db_refresh or db_refresh.is_revoked:
        raise ValueError("Refresh token revoked or not found")
    expires_at = db_refresh.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise ValueError("Refresh token expired")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise ValueError("User not found or inactive")

    return issue_token_pair(db, user)


def revoke_refresh_token(db: Session, refresh_token: str) -> None:
    token_hash = _hash_token(refresh_token)
    db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).update({RefreshToken.is_revoked: True})
    db.commit()


def decode_access_token(token: str, secret_key: str, algorithm: str) -> dict:
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    if payload.get("typ") != "access":
        raise ValueError("Invalid access token type")
    return payload
