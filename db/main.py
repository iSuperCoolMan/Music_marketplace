from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import Base
from settings import directories


engine = create_engine(directories.DB_DIRECTORY, echo=True)

Base.metadata.create_all(engine)


def commit_after(func):
    async def wrapper(*args, **kwargs):
        with Session(engine) as session:
            try:
                result = await func(session, *args, **kwargs)
            except:
                session.rollback()
                raise
            else:
                session.commit()
                return result

    return wrapper


def set_session(func):
    async def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return await func(session, *args, **kwargs)

    return wrapper