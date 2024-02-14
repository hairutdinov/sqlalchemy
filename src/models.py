from datetime import datetime
from enum import Enum
from typing import Annotated
from typing import Optional

from database import Base
from database import str_256
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import CheckConstraint
from sqlalchemy import Index
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
    __table_args__ = (
        Index("resumes_title_idx", "title"),
        CheckConstraint("compensation > 0", name="resumes_check_compensation_gt_0")
    )

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

    vacancies_replied: Mapped[list["Vacancies"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

    include_repr_columns = ("workload",)


class Vacancies(Base):
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]

    resumes_replied: Mapped[list["Resumes"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )


class VacanciesReplies(Base):
    __tablename__ = "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cover_letter: Mapped[Optional[str]]


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)