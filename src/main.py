import os
import sys

from queries.core import Core

# from queries.core import create_tables
# from queries.core import drop_tables
# from queries.core import insert_test_data

sys.path.insert(1, os.path.join(sys.path[0], ".."))

Core.recreate_tables()
Core.insert_workers()
Core.update_worker(1)
Core.select_workers()
