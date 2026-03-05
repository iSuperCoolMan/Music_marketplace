from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.main import commit_after, set_session
from db.models import SupportChatSessionBase, UserBase
from models.message import Message
from models.support_chat_session import SupportChatSession


@commit_after
async def create_chat_session(session: Session, ip: str, user_uuid: UUID | None = None) -> SupportChatSession:
    if user_uuid:
        statement = select(UserBase).where(UserBase.uuid == user_uuid)
        user = session.scalars(statement).one_or_none()
    else:
        user = None

    chat_session = SupportChatSessionBase(
        uuid=uuid4(),
        user=user,
        ip=ip
    )

    session.add(chat_session)

    if user:
        user.support_chat_sessions.append(chat_session)

    return SupportChatSession(
        uuid=chat_session.uuid,
        ip=chat_session.ip,
        user_uuid=chat_session.user_uuid,
        messages=[]
    )


@set_session
async def get_chat_session_by_uuid(session: Session, uuid: UUID) -> SupportChatSession | None:
    statement = select(SupportChatSessionBase).where(SupportChatSessionBase.uuid == uuid)
    chat_session = session.scalars(statement).one_or_none()

    if chat_session is None:
        return None

    return SupportChatSession(
        uuid=chat_session.uuid,
        ip=chat_session.ip,
        user_uuid=chat_session.user_uuid,
        messages=[Message(
            uuid=message.uuid,
            text=message.text,
            date_time=message.date_time.strftime("%H:%M:%S"),
            user_uuid=message.user_uuid,
            session_uuid=message.session_uuid
        ) for message in chat_session.messages]
    )