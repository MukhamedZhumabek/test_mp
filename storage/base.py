from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from settings import sqlalchemy_url

engine = create_async_engine(sqlalchemy_url)

async_session = async_sessionmaker(engine, expire_on_commit=False)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    def __init__(self, **kw):
        for col in self.__table__.columns.keys():
            setattr(self, col, kw.get(col))
