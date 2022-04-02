import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Hack to determine if we are running tests, and if we are put the engine in memory
# so as not to interfere with the user's actual information
if "pytest" in sys.modules:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
else:
    engine = create_engine("sqlite+pysqlite:///rsl.db", future=True)

Base = declarative_base()