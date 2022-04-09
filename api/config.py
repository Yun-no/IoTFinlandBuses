import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')
    number_of_records: int = Field(..., env='NUMBER_OF_RECORDS')
    valid_time_range: int = Field(..., env='VALID_TIME_RANGE')

settings = Settings()
