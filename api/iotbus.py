from fastapi import Depends, APIRouter
from models import AreaRange
from db import BusPosition
from config import settings
from datetime import datetime, timedelta

iotbus_route = APIRouter()


@iotbus_route.post('/busaround')
async def create_label(area_range: AreaRange):
    # get the settings time range for filtering
    since = datetime.now() - timedelta(minutes=settings.valid_time_range)

    # limit the number of return records by settings
    record_limit = settings.number_of_records

    # read from database
    return await BusPosition.objects.filter(((BusPosition.latitude >= area_range.latitude_from) &
                                             (BusPosition.latitude <= area_range.latitude_to) &
                                             (BusPosition.longitude >= area_range.longitude_from) &
                                             (BusPosition.longitude <= area_range.longitude_to) &
                                             (BusPosition.updated >= since))).limit(record_limit).all()
