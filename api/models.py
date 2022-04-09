from pydantic import BaseModel


class AreaRange(BaseModel):
    latitude_from: float
    latitude_to: float
    longitude_from: float
    longitude_to: float
