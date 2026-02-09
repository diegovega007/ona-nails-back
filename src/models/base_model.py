from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False)
    modified_at: Optional[datetime] = Field(nullable=True)