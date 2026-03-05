from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.main import commit_after
from db.models import MessageBase, SupportChatSessionBase, UserBase


@commit_after
async def try_create_message(
        session: Session,
        text: str,
        date_time: datetime,
        session_uuid: UUID,
        from_support: bool,
        user_uuid: UUID | None = None
) -> bool:
    statement = select(SupportChatSessionBase).where(SupportChatSessionBase.uuid == session_uuid)
    chat_session = session.scalars(statement).one_or_none()

    if chat_session is None:
        return False

    if user_uuid:
        statement = select(UserBase).where(UserBase.uuid == user_uuid)
        user = session.scalars(statement).one_or_none()
    else:
        user = None

    message = MessageBase(
        uuid=uuid4(),
        text=text,
        date_time=date_time,
        user=user,
        from_support=from_support,
        session=chat_session,
    )

    session.add(message)
    chat_session.messages.append(message)

    if user:
        user.messages.append(message)

    return True