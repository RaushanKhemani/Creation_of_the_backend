import asyncio
import logging
from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from sqlalchemy.orm import Session

from config import get_settings
from db.models.conversation import Chat
from db.models.message import Message
from db.models.provider import AIProvider
from db.models.usage_log import UsageLog
from db.models.user import User
from schemas.chat import ChatRouteRequest, ChatRouteResponse, ChatWindowCreateRequest, ChatWindowRead, MessageRead
from services.integration_service import get_active_integration_record, normalize_provider_key
from services.provider_gateway import ProviderGateway

logger = logging.getLogger("ai_hub.chat")
provider_gateway = ProviderGateway()

COST_PER_1K_TOKENS_USD = {
    "chatgpt": 0.002,
    "gemini": 0.001,
    "claude": 0.003,
    "grok": 0.0025,
    "groq": 0.0015,
}


def _make_title(prompt: str) -> str:
    compact = " ".join(prompt.split())
    return compact[:80] if len(compact) > 80 else compact


def create_chat_window(db: Session, user: User, payload: ChatWindowCreateRequest, provider_key: str) -> ChatWindowRead:
    chat = Chat(user_id=user.id, title=payload.title.strip(), provider_key=provider_key)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return ChatWindowRead.model_validate(chat)


def list_chat_windows(db: Session, user: User) -> list[ChatWindowRead]:
    rows = db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.updated_at.desc()).all()
    return [ChatWindowRead.model_validate(item) for item in rows]


def list_chat_messages(db: Session, user_id: int, chat_id: int) -> list[MessageRead]:
    rows = db.query(Message).filter(Message.user_id == user_id, Message.chat_id == chat_id).order_by(Message.id.asc()).all()
    return [MessageRead.model_validate(row) for row in rows]


async def _generate_with_retry(provider_key: str, prompt: str, api_key: str | None):
    settings = get_settings()
    attempts = settings.provider_max_retries + 1

    for attempt in range(1, attempts + 1):
        try:
            return await asyncio.wait_for(
                provider_gateway.generate(provider_key, prompt, api_key),
                timeout=settings.provider_timeout_seconds,
            )
        except Exception:
            if attempt >= attempts:
                raise
            await asyncio.sleep(0.2 * attempt)


def _resolve_provider(db: Session, user: User, payload: ChatRouteRequest):
    active = get_active_integration_record(db, user)
    if not active:
        raise ValueError("No active API key configured. Add API key in /api/v1/integrations/api-key")

    selected_provider_key = active.provider_key
    if payload.provider_key:
        requested = normalize_provider_key(payload.provider_key)
        if requested != selected_provider_key:
            raise ValueError("Requested provider does not match your active API key provider")
        selected_provider_key = requested

    provider = db.query(AIProvider).filter(AIProvider.key == selected_provider_key, AIProvider.enabled.is_(True)).first()
    if not provider:
        raise ValueError("Provider unavailable")

    return provider, active


def _resolve_chat(db: Session, user: User, chat_id: int | None, provider_key: str, prompt: str) -> Chat:
    if chat_id:
        existing = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
        if existing:
            return existing

    chat = Chat(user_id=user.id, title=_make_title(prompt), provider_key=provider_key)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


async def route_chat(db: Session, user: User, payload: ChatRouteRequest) -> ChatRouteResponse:
    request_id = uuid4().hex
    started = perf_counter()

    provider, active_integration = _resolve_provider(db, user, payload)
    chat = _resolve_chat(db, user, payload.chat_id, provider.key, payload.prompt)

    user_msg = Message(
        chat_id=chat.id,
        user_id=user.id,
        role="user",
        content=payload.prompt,
        provider_key=provider.key,
        model_name=f"{provider.key}-simulated-v1",
    )
    db.add(user_msg)
    db.commit()

    try:
        provider_result = await _generate_with_retry(provider.key, payload.prompt, active_integration.api_key_plain)
        elapsed_ms = int((perf_counter() - started) * 1000)
        rate = COST_PER_1K_TOKENS_USD.get(provider.key, 0.002)
        cost_usd = round((provider_result.tokens_out / 1000) * rate, 6)

        assistant_msg = Message(
            chat_id=chat.id,
            user_id=user.id,
            role="assistant",
            content=provider_result.text,
            provider_key=provider.key,
            model_name=provider_result.model_name,
            latency_ms=elapsed_ms,
            tokens_in=provider_result.tokens_in,
            tokens_out=provider_result.tokens_out,
            cost_usd=cost_usd,
        )
        usage = UsageLog(
            request_id=request_id,
            user_id=user.id,
            chat_id=chat.id,
            provider_key=provider.key,
            model_name=provider_result.model_name,
            status="success",
            latency_ms=elapsed_ms,
            tokens_in=provider_result.tokens_in,
            tokens_out=provider_result.tokens_out,
            cost_usd=cost_usd,
        )
        db.add(assistant_msg)
        db.add(usage)
        db.commit()

        logger.info(
            "chat_completed",
            extra={
                "request_id": request_id,
                "user_id": user.id,
                "model": provider_result.model_name,
                "latency_ms": elapsed_ms,
                "tokens_in": provider_result.tokens_in,
                "tokens_out": provider_result.tokens_out,
                "cost_usd": cost_usd,
            },
        )

        return ChatRouteResponse(
            request_id=request_id,
            chat_id=chat.id,
            provider_key=provider.key,
            model_name=provider_result.model_name,
            answer=provider_result.text,
            latency_ms=elapsed_ms,
            tokens_in=provider_result.tokens_in,
            tokens_out=provider_result.tokens_out,
            cost_usd=cost_usd,
            created_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        elapsed_ms = int((perf_counter() - started) * 1000)
        db.add(
            UsageLog(
                request_id=request_id,
                user_id=user.id,
                chat_id=chat.id,
                provider_key=provider.key,
                model_name=f"{provider.key}-simulated-v1",
                status="failed",
                latency_ms=elapsed_ms,
                error_message=str(exc),
            )
        )
        db.commit()
        raise
