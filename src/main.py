import os
import sys
from queries.core import create_tables
from queries.core import drop_tables
from queries.core import insert_test_data

sys.path.insert(1, os.path.join(sys.path[0], '..'))

drop_tables()
create_tables()
insert_test_data()
