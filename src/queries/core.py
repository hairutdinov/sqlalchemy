from pathlib import Path
from sqlalchemy import text, insert

import models
from database import engine
from models import metadata_obj


def create_tables():
    engine.echo = False
    metadata_obj.create_all(engine)
    engine.echo = True


def drop_tables():
    engine.echo = False
    metadata_obj.drop_all(engine)
    engine.echo = True


def insert_test_data():
    sql_stmt = insert(models.workers_table).values([
        {"username": "Bobr"},
        {"username": "Volk"},
    ])
    with engine.connect() as conn:
        conn.execute(sql_stmt)
        conn.commit()
