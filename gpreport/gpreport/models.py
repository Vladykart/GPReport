from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, ARRAY


Base = declarative_base()


class StationsForecast(Base):
    __tablename__ = "pvforecast_in_garpok"

    pv_forecast_result2_id = Column("id", Integer, primary_key=True)
    date_time_forecast = Column("dt", DateTime)
    rdn = Column("rdn", Integer)
    vdr = Column("vdr", Integer)
    station_id = Column("id_st", Integer)
