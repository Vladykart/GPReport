from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StationsForecast(BaseModel):

    date_time_forecast: datetime
    station_id: int
    vdr: Optional[int]
    rdn: Optional[int]

    class Config:
        orm_mode = True


