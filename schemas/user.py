from datetime import datetime

from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {"from_attributes": True}
