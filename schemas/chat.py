from datetime import datetime

from pydantic import BaseModel, Field


class ChatWindowCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class ChatWindowRead(BaseModel):
    id: int
    title: str
    provider_key: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRouteRequest(BaseModel):
    provider_key: str | None = Field(default=None, min_length=2, max_length=64)
    prompt: str = Field(min_length=1, max_length=8000)
    chat_id: int | None = None


class ChatRouteResponse(BaseModel):
    request_id: str
    chat_id: int
    provider_key: str
    model_name: str
    answer: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    created_at: datetime


class MessageRead(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    provider_key: str
    model_name: str
    latency_ms: int | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
