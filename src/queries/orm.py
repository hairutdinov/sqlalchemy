from database import Base
from database import engine
from database import session_factory
from models import Resumes
from models import Workers
from models import Workload
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload


class Core:
    @staticmethod
    def recreate_tables():
        engine.echo = False
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_jack = Workers(username="jack")
            worker_michael = Workers(username="michael")
            # session.add(worker_jack)
            # session.add(worker_michael)
            session.add_all([worker_jack, worker_michael])
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(Workers)
            result = session.execute(query)
            print(result.scalars().all())

    @staticmethod
    def update_worker(worker_id: int = 1, username: str = "emanuel"):
        with session_factory() as session:
            worker_michael = session.get(Workers, worker_id)
            worker_michael.username = username
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = Resumes(
                title="Python Junior Developer",
                compensation=50000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            resume_jack_2 = Resumes(
                title="Python Разработчик",
                compensation=150000,
                workload=Workload.fulltime,
                worker_id=1,
            )
            resume_michael_1 = Resumes(
                title="Python Data Engineer",
                compensation=250000,
                workload=Workload.parttime,
                worker_id=2,
            )
            resume_michael_2 = Resumes(
                title="Data Scientist",
                compensation=300000,
                workload=Workload.fulltime,
                worker_id=2,
            )
            session.add_all(
                [resume_jack_1, resume_jack_2, resume_michael_1, resume_michael_2]
            )
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        with session_factory() as session:
            """
            SELECT resumes.workload, CAST(avg(resumes.compensation) AS INTEGER) AS avg_compensation
            FROM resumes
            WHERE (resumes.title LIKE '%' || 'Python' || '%') AND resumes.compensation > 40000
            GROUP BY resumes.workload
            """
            query = (
                select(
                    Resumes.workload,
                    func.cast(func.avg(Resumes.compensation), Integer).label(
                        "avg_compensation"
                    ),
                )
                .select_from(Resumes)
                .filter(
                    and_(
                        Resumes.title.contains(like_language),
                        Resumes.compensation > 40000,
                    )
                )
                .group_by(Resumes.workload)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},  # id 5
            ]
            resumes = [
                {
                    "title": "Python программист",
                    "compensation": 60000,
                    "workload": "fulltime",
                    "worker_id": 3,
                },
                {
                    "title": "Machine Learning Engineer",
                    "compensation": 70000,
                    "workload": "parttime",
                    "worker_id": 3,
                },
                {
                    "title": "Python Data Scientist",
                    "compensation": 80000,
                    "workload": "parttime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Analyst",
                    "compensation": 90000,
                    "workload": "fulltime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Junior Developer",
                    "compensation": 100000,
                    "workload": "fulltime",
                    "worker_id": 5,
                },
            ]
            insert_workers = insert(Workers).values(workers)
            insert_resumes = insert(Resumes).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func(like_language: str = "Python"):
        with session_factory() as session:
            r = aliased(Resumes)
            w = aliased(Workers)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)
                    .over(partition_by=r.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                # .select_from(r)
                .join(
                    r, r.worker_id == w.id
                ).subquery(  # default - INNER, full=True - FULL JOIN, isouter=True - LEFT JOIN, нет RIGHT JOIN'а
                    "helper1"
                )
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.id,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())
            print(query.compile(compile_kwargs={"literal_binds": True}))
            print(session.execute(query).all())

    @staticmethod
    def select_workers_lazy_relationship():
        with session_factory() as session:
            query = select(Workers)
            res = session.execute(query)
            result = res.scalars().all()
            print(result[0].resumes)

    @staticmethod
    def select_workers_joined_relationship():
        with session_factory() as session:
            query = select(Workers).options(joinedload(Workers.resumes))
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result[0].resumes)

    @staticmethod
    def select_workers_selectin_relationship():
        with session_factory() as session:
            query = select(Workers).options(selectinload(Workers.resumes))
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result[0].resumes)
