import os
import sys

from queries.orm import Core

sys.path.insert(1, os.path.join(sys.path[0], ".."))

Core.recreate_tables()
Core.insert_workers()
Core.insert_resumes()
Core.update_worker(2)
Core.select_workers()
Core.select_resumes_avg_compensation()
