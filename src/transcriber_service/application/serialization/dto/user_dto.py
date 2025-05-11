from pydantic import BaseModel, Field
from datetime import datetime


class UserDTO(BaseModel):
    entity_type: str = Field(..., pattern="^(auth_user|admin)$")
    id: str
    email: str
    password_hash: str
    registration_date: datetime
    last_updated: datetime
    is_blocked: bool
    temp_password_hash: str | None = None

    class Config:
        from_attributes = True
