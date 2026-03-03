from datetime import datetime

from pydantic import BaseModel, Field


class ChatRouteRequest(BaseModel):
    provider_key: str | None = Field(default=None, min_length=2, max_length=64)
    prompt: str = Field(min_length=1, max_length=8000)
    conversation_id: int | None = None


class ChatRouteResponse(BaseModel):
    request_id: str
    conversation_id: int
    provider_key: str
    answer: str
    latency_ms: int
    source: str
    created_at: datetime


class MessageRead(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    provider_key: str
    latency_ms: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
