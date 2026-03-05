from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    uuid: UUID
    text: str
    date_time: datetime
    user_uuid: UUID | None
    session_uuid: UUID