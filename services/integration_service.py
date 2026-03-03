from hashlib import sha256

from sqlalchemy.orm import Session

from db.models.user import User
from db.models.user_api_key import UserAPIKey
from schemas.integration import APIKeyRegisterResponse, ActiveIntegrationResponse


def normalize_provider_key(provider_key: str) -> str:
    key = provider_key.strip().lower()
    mapping = {
        "openai": "chatgpt",
        "chatgpt": "chatgpt",
        "gemini": "gemini",
        "grok": "grok",
        "xai": "grok",
        "claude": "claude",
        "clawd": "claude",
        "anthropic": "claude",
    }
    return mapping.get(key, key)


def detect_provider_from_api_key(api_key: str) -> tuple[str, str]:
    key = api_key.strip()
    lowered = key.lower()

    if key.startswith("sk-ant-"):
        return "claude", "claude"
    if key.startswith("AIza"):
        return "gemini", "gemini"
    if lowered.startswith("xai-") or lowered.startswith("sk-xai-"):
        return "grok", "grok"
    if key.startswith("sk-"):
        return "openai", "chatgpt"

    raise ValueError("Could not recognize provider from API key")


def _mask_api_key(api_key: str) -> str:
    key = api_key.strip()
    if len(key) <= 8:
        return "*" * len(key)
    return f"{key[:4]}...{key[-4:]}"


def register_api_key(db: Session, user: User, api_key: str) -> APIKeyRegisterResponse:
    provider_name, provider_key = detect_provider_from_api_key(api_key)
    # Scope digest by user id so two users can register the same provider key format
    # without hitting a global unique constraint.
    digest = sha256(f"{user.id}:{api_key}".encode("utf-8")).hexdigest()
    masked = _mask_api_key(api_key)

    db.query(UserAPIKey).filter(UserAPIKey.user_id == user.id).update({UserAPIKey.is_active: False})

    existing = db.query(UserAPIKey).filter(UserAPIKey.api_key_hash == digest, UserAPIKey.user_id == user.id).first()
    if existing:
        existing.provider_name = provider_name
        existing.provider_key = provider_key
        existing.api_key_masked = masked
        existing.is_active = True
    else:
        db.add(
            UserAPIKey(
                user_id=user.id,
                provider_name=provider_name,
                provider_key=provider_key,
                api_key_hash=digest,
                api_key_masked=masked,
                is_active=True,
            )
        )

    db.commit()
    return APIKeyRegisterResponse(provider_name=provider_name, provider_key=provider_key, api_key_masked=masked)


def get_active_integration(db: Session, user: User) -> ActiveIntegrationResponse | None:
    row = (
        db.query(UserAPIKey)
        .filter(UserAPIKey.user_id == user.id, UserAPIKey.is_active.is_(True))
        .order_by(UserAPIKey.updated_at.desc())
        .first()
    )
    if not row:
        return None
    return ActiveIntegrationResponse(
        provider_name=row.provider_name,
        provider_key=row.provider_key,
        api_key_masked=row.api_key_masked,
        is_active=row.is_active,
    )


def get_active_provider_key(db: Session, user_id: int) -> str | None:
    row = (
        db.query(UserAPIKey)
        .filter(UserAPIKey.user_id == user_id, UserAPIKey.is_active.is_(True))
        .order_by(UserAPIKey.updated_at.desc())
        .first()
    )
    if not row:
        return None
    return row.provider_key
