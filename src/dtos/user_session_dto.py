from pydantic import BaseModel
from datetime import datetime
from typing import Text

class CreateUserSessionDTO(BaseModel):
    user_id: int
    refresh_token: str
    ip_address: str
    user_agent: Text
    expires_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "refresh_token": "refresh_token",
                "ip_address": "127.0.0.1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "expires_at": "2021-01-01T00:00:00Z"
            }
        }
