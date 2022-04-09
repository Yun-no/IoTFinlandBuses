import databases
import ormar
import sqlalchemy
from datetime import datetime
from config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class BusPosition(ormar.Model):
    class Meta(BaseMeta):
        tablename = "bus_positions"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    bus_id: str = ormar.String(unique=True, index=True, max_length=500)
    latitude: float = ormar.Float(index=True)
    longitude: float = ormar.Float(index=True)
    next_stop: str = ormar.String(max_length=500, nullable=True)
    updated: datetime = ormar.DateTime(index=True)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.drop_all(engine)
metadata.create_all(engine)
