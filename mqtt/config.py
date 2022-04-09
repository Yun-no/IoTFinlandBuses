import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mqtt_broker_address: str = Field(..., env='MQTT_BROKER_ADDRESS')
    mqtt_broker_port: int = Field(..., env='MQTT_BROKER_PORT')
    mqtt_broker_topic: str = Field(..., env='MQTT_BROKER_TOPIC')

    db_name: str = Field(..., env='DB_NAME')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    db_host: str = Field(..., env='DB_HOST')
    db_port: int = Field(..., env='DB_PORT')


settings = Settings()
