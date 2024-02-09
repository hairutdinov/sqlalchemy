from pathlib import Path
from sqlalchemy import text, insert

from database import engine, session_factory
from models import Workers
from database import Base


def create_tables():
    engine.echo = False
    Base.metadata.create_all(engine)
    engine.echo = True


def drop_tables():
    engine.echo = False
    Base.metadata.drop_all(engine)
    engine.echo = True


def insert_test_data():
    with session_factory() as session:
        worker_bobr = Workers(username="bobr")
        worker_volk = Workers(username="volk")
        # session.add(worker_bobr)
        # session.add(worker_volk)
        session.add_all([worker_bobr, worker_volk])
        session.commit()
