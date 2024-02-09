# import asyncio
from typing import Annotated

from config import settings
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import Session

engine = create_engine(
    url=settings.DATABASE_URL_psycopg, echo=True, pool_size=5, max_overflow=10
)

session_factory = sessionmaker(engine)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}


if __name__ == "__main__":
    with engine.connect() as conn:
        res = conn.execute(text("SELECT 1, 2, 3 UNION SELECT 4, 5, 6"))
        print(f"{res.all()=}")
        conn.commit()
