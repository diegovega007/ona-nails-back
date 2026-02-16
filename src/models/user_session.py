from .base_model import BaseModel
from sqlmodel import Field, Relationship
from datetime import datetime
from typing import Text, Optional
from .user import User

class UserSession(BaseModel, table=True):
    __tablename__ = "user_sessions"

    id: int = Field(nullable=False, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id")
    refresh_token: str = Field(nullable=False)
    ip_address: str = Field(nullable=False, max_length=50)
    user_agent: Text = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    is_revoked: bool = Field(nullable=False, default=False)

    user: Optional["User"] = Relationship()