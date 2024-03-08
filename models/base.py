from typing import Any

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'

    async def save(self, db_session: AsyncSession):
        db_session.add(self)
        return await db_session.commit()

    async def delete(self, db_session: AsyncSession):
        await db_session.delete(self)
        await db_session.commit()
        return True

    async def update(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return await db.commit()

    async def save_or_update(self, db: AsyncSession):
        try:
            db.add(self)
            return await db.commit()
        except IntegrityError as exception:
            if isinstance(exception.orig, UniqueViolationError):
                return await db.merge(self)
        finally:
            await db.close()
