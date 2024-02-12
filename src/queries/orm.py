from database import Base
from database import engine
from database import session_factory
from models import Workers
from sqlalchemy import select


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
