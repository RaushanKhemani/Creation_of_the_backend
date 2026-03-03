from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from db.models.conversation import Conversation
from db.models.message import Message
from db.models.provider import AIProvider
from db.models.usage_log import UsageLog
from db.models.user import User
from schemas.chat import ChatRouteRequest, ChatRouteResponse, MessageRead
from services.integration_service import get_active_provider_key, normalize_provider_key
from services.provider_gateway import ProviderGateway

provider_gateway = ProviderGateway()


def _make_title(prompt: str) -> str:
    compact = " ".join(prompt.split())
    return compact[:80] if len(compact) > 80 else compact


def _get_or_create_conversation(
    db: Session, user: User, payload: ChatRouteRequest, selected_provider_key: str
) -> Conversation:
    if payload.conversation_id:
        existing = (
            db.query(Conversation)
            .filter(Conversation.id == payload.conversation_id, Conversation.user_id == user.id)
            .first()
        )
        if existing:
            return existing

    conv = Conversation(user_id=user.id, title=_make_title(payload.prompt), provider_key=selected_provider_key)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def list_conversation_messages(db: Session, user_id: int, conversation_id: int) -> list[MessageRead]:
    rows = (
        db.query(Message)
        .filter(Message.user_id == user_id, Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
        .all()
    )
    return [MessageRead.model_validate(row) for row in rows]


def route_chat(db: Session, user: User, payload: ChatRouteRequest) -> ChatRouteResponse:
    request_id = uuid4().hex
    started = perf_counter()

    active_provider_key = get_active_provider_key(db, user.id)
    if not active_provider_key:
        raise ValueError("No active API key configured. Add API key in /api/v1/integrations/api-key")

    selected_provider_key = active_provider_key
    if payload.provider_key:
        requested_provider_key = normalize_provider_key(payload.provider_key)
        if requested_provider_key != active_provider_key:
            raise ValueError("Requested provider does not match your active API key provider")
        selected_provider_key = requested_provider_key

    provider = db.query(AIProvider).filter(AIProvider.key == selected_provider_key).first()
    if not provider or not provider.enabled:
        db.add(
            UsageLog(
                request_id=request_id,
                user_id=user.id,
                provider_key=selected_provider_key,
                status="failed",
                error_message="Provider unavailable",
            )
        )
        db.commit()
        raise ValueError("Provider unavailable")

    conversation = _get_or_create_conversation(db, user, payload, selected_provider_key)

    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user.id,
        role="user",
        content=payload.prompt,
        provider_key=selected_provider_key,
    )
    db.add(user_msg)
    db.commit()

    try:
        provider_result = provider_gateway.generate(selected_provider_key, payload.prompt)
        elapsed_ms = int((perf_counter() - started) * 1000)

        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user.id,
            role="assistant",
            content=provider_result.text,
            provider_key=selected_provider_key,
            latency_ms=elapsed_ms,
            tokens_in=provider_result.tokens_in,
            tokens_out=provider_result.tokens_out,
        )
        usage = UsageLog(
            request_id=request_id,
            user_id=user.id,
            provider_key=selected_provider_key,
            status="success",
            latency_ms=elapsed_ms,
        )
        db.add(assistant_msg)
        db.add(usage)
        db.commit()

        return ChatRouteResponse(
            request_id=request_id,
            conversation_id=conversation.id,
            provider_key=selected_provider_key,
            answer=provider_result.text,
            latency_ms=elapsed_ms,
            source=provider_result.source,
            created_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        elapsed_ms = int((perf_counter() - started) * 1000)
        db.add(
            UsageLog(
                request_id=request_id,
                user_id=user.id,
                provider_key=selected_provider_key,
                status="failed",
                latency_ms=elapsed_ms,
                error_message=str(exc),
            )
        )
        db.commit()
        raise
