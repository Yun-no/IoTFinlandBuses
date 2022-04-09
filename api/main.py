from fastapi import FastAPI
from datetime import datetime
from iotbus import iotbus_route
from db import database, BusPosition


app = FastAPI()

app.include_router(iotbus_route, prefix='/api/v1', tags=['iotbus'])


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await BusPosition.objects.get_or_create(bus_id='dummy_bus_id', latitude=60.170519,
                                            longitude=24.942734, next_stop='dummy_bus_stop', updated=datetime.now())


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


