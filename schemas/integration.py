from pydantic import BaseModel, Field


class APIKeyRegisterRequest(BaseModel):
    api_key: str = Field(min_length=8, max_length=300)


class APIKeyRegisterResponse(BaseModel):
    provider_name: str
    provider_key: str
    api_key_masked: str
    chat_enabled: bool = True


class ActiveIntegrationResponse(BaseModel):
    provider_name: str
    provider_key: str
    api_key_masked: str
    is_active: bool
