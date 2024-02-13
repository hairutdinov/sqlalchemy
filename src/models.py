from datetime import datetime
from enum import Enum
from typing import Annotated

from database import Base
from database import str_256
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow()
    ),
]


class Workers(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["Resumes"]] = relationship(
        back_populates="worker"
    )

    resumes_parttime: Mapped[list["Resumes"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(Workers.id == Resumes.worker_id, Resumes.workload == 'parttime')",
        order_by="Resumes.id.desc()"
    )


class Workload(Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class Resumes(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    # compensation: Mapped[int] = mapped_column(nullable=True)
    # compensation: Mapped[Optional[int]]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["Workers"] = relationship(
        back_populates="resumes"
    )

    include_repr_columns = ("workload",)


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
