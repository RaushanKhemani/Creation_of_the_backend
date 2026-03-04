from sqlalchemy.orm import Session

from db.models.provider import AIProvider
from schemas.provider import ProviderCreate

DEFAULT_PROVIDERS = [
    {
        "key": "chatgpt",
        "name": "ChatGPT",
        "category": "general_assistant",
        "enabled": True,
        "notes": "Planning, ideation, and broad Q&A.",
    },
    {
        "key": "copilot",
        "name": "GitHub Copilot",
        "category": "coding",
        "enabled": True,
        "notes": "Code generation and developer workflow support.",
    },
    {
        "key": "gemini",
        "name": "Gemini",
        "category": "coding",
        "enabled": True,
        "notes": "Alternative coding and multimodal workflows.",
    },
    {
        "key": "grok",
        "name": "Grok",
        "category": "design_brainstorming",
        "enabled": True,
        "notes": "Creative brainstorming and concept exploration.",
    },
    {
        "key": "claude",
        "name": "Claude",
        "category": "general_assistant",
        "enabled": True,
        "notes": "Reasoning-focused assistant from Anthropic.",
    },
    {
        "key": "groq",
        "name": "Groq",
        "category": "low_latency_inference",
        "enabled": True,
        "notes": "Low-latency inference provider.",
    },
]


def list_providers(db: Session) -> list[AIProvider]:
    return db.query(AIProvider).order_by(AIProvider.name.asc()).all()


def get_provider_by_key(db: Session, provider_key: str) -> AIProvider | None:
    return db.query(AIProvider).filter(AIProvider.key == provider_key).first()


def create_provider(db: Session, payload: ProviderCreate) -> AIProvider | None:
    existing = get_provider_by_key(db, payload.key)
    if existing:
        return None

    provider = AIProvider(**payload.model_dump())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def seed_default_providers(db: Session) -> None:
    existing_keys = {row.key for row in db.query(AIProvider.key).all()}
    changed = False

    for item in DEFAULT_PROVIDERS:
        if item["key"] in existing_keys:
            continue
        db.add(AIProvider(**item))
        changed = True

    if changed:
        db.commit()
