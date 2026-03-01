from db.base import Base
from db.models import AIProvider, Conversation, Message, UsageLog, User
from db.session import SessionLocal, get_engine
from services.provider_service import seed_default_providers


def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())
    with SessionLocal() as db:
        seed_default_providers(db)
