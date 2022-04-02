from ._db_core import engine, Base
from .ratings import Rating
from .champion import Champion, OwnedChampion

Base.metadata.create_all(engine)