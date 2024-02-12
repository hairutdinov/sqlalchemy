import models
from database import engine
from models import metadata_obj
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update


class Core:
    @staticmethod
    def recreate_tables():
        engine.echo = False
        metadata_obj.drop_all(engine)
        metadata_obj.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_workers():
        sql_stmt = insert(models.workers_table).values(
            [
                {"username": "Jack"},
                {"username": "Michael"},
            ]
        )
        with engine.connect() as conn:
            conn.execute(sql_stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with engine.connect() as conn:
            query = select(models.workers_table)
            result = conn.execute(query)
            print(result.all())

    @staticmethod
    def update_worker(worker_id: int = 1, username: str = "Emanuel"):
        with engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username where id=:id")
            # stmt = stmt.bindparams(username=username, id=worker_id)
            # conn.execute(stmt)
            # conn.commit()
            stmt = (
                update(models.workers_table).values(username=username)
                # .where(models.workers_table.c.id == worker_id)
                # .filter(models.workers_table.c.id == worker_id)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()
