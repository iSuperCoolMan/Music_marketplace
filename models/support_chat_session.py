from uuid import UUID

from pydantic import BaseModel

from models.message import Message


class SupportChatSession(BaseModel):
    uuid: UUID
    ip: str
    user_uuid: str | None
    messages: list[Message]