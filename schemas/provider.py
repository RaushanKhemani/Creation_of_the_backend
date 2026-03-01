from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    key: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=128)
    category: str = Field(min_length=2, max_length=64)
    enabled: bool = True
    notes: str | None = Field(default=None, max_length=500)


class ProviderRead(ProviderCreate):
    id: int

    model_config = {"from_attributes": True}
