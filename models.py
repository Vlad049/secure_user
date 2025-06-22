from typing import List, Optional, Union
from uuid import uuid4
import asyncio

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from pydantic_models import settings


engine =  create_async_engine(settings.sqlalchemy_uri, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(15))
    address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)
    user_id: Mapped[str] = mapped_column(String(100))

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    token: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)

    def __init__(self, **kwargs):
        self.id = uuid4().hex
        super().__init__(**kwargs)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session


if __name__ == "__main__":
    asyncio.run(create_db())