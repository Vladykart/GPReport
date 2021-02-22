from time import sleep
import sqlalchemy
from time import sleep
from datetime import datetime

import sqlalchemy
from sqlalchemy import create_engine, and_
from sqlalchemy import update
from sqlalchemy.orm import Session

from models import StationsForecast as ModelStationsForecast
from schemas import StationsForecast as SchemaStationsForecast

# cnf = FactoryConfig(GlobalDBConfig().ENV_STATE)()

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://"
    + 'LOGIN'
    + ":"
    + 'PASSWORD'
    + "@"
    + 'HOST'
    + ":"
    + str(PORT)
    + "/"
    + 'DASTABASE'
)
metadata = sqlalchemy.MetaData()

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = Session(autocommit=False, autoflush=False, bind=engine)


# def update_station_forecast(
#     station_id: int,
#     datetime_format: datetime,
#     new_values:ModelStationsForecast,
#     db: Session = session,
# ):
#     forecast = db.query(ModelStationsForecast).filter(
#         and_(
#             ModelStationsForecast.station_id == station_id,
#             ModelStationsForecast.date_time_forecast == datetime_format,
#         )
#     ).first().update()
#     forecast = new_values


def check_forecast_is_exists(
    date_time_forecast: datetime,
    station_id: int,
    db: Session = session,
):
    exist = (
        db.query(ModelStationsForecast)
            .filter(
            and_(
                ModelStationsForecast.date_time_forecast == date_time_forecast,
                ModelStationsForecast.station_id == station_id,
            )
        )
            .first()
    )
    sleep(1)
    if exist is not None:
        return exist
    else:
        return False


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def find_index(dicts, key, value):
    class Null:
        pass

    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i
        else:
            raise ValueError("no dict with the key and value combination found")


def write_rdn_for_tomorrow(
    data,
    station_id,
    db: Session = session,
):
    if data is not None:
        for rdn in data:
            for i in range(24):
                station_forecast = SchemaStationsForecast(
                    station_id=station_id,
                    date_time_forecast=datetime.combine(
                        datetime.strptime(rdn["date"], "%d-%m-%Y").date(),
                        datetime.strptime(str(i), "%H").time(),
                    ),
                    rdn=rdn["data_frame"][i],
                    vdr=0
                )
                db_station_forecast = ModelStationsForecast(
                    date_time_forecast=station_forecast.date_time_forecast,
                    station_id=station_forecast.station_id,
                    rdn=station_forecast.rdn,
                    vdr=station_forecast.vdr,
                )
                if (
                    check_forecast_is_exists(
                        station_forecast.date_time_forecast,
                        station_forecast.station_id,
                    )
                    is False
                ):
                    db.add(db_station_forecast)
                    print(
                        f"add: {station_forecast.station_id}, {station_forecast.date_time_forecast}"
                    )
                    print(
                        "rdn = ",
                        rdn["data_frame"][i],
                    )
                else:
                    print(
                        f"is exist: {station_forecast.station_id}, {station_forecast.date_time_forecast}"
                    )
            db.commit()
        db.close()
    else:
        pass


def create_station_forecast(
    data,
    station_id,
    db: Session = session,
):
    for vdr_rdn in data:
        date = vdr_rdn["date"]

        for i in range(24):
            vdr_dataframe_by_date = build_dict(vdr_rdn["vdr"], key="date")
            rdn_dataframe_by_date = build_dict(vdr_rdn["rdn"], key="date")
            station_forecast = SchemaStationsForecast(
                station_id=station_id,
                date_time_forecast=datetime.combine(
                    datetime.strptime(vdr_rdn["date"], "%d-%m-%Y").date(),
                    datetime.strptime(str(i), "%H").time(),
                ),
                vdr=vdr_dataframe_by_date.get(date)["data_frame"][i],
                rdn=rdn_dataframe_by_date.get(date)["data_frame"][i],
            )

            db_station_forecast = ModelStationsForecast(
                date_time_forecast=station_forecast.date_time_forecast,
                station_id=station_forecast.station_id,
                rdn=station_forecast.rdn,
                vdr=station_forecast.vdr,
            )
            exist = check_forecast_is_exists(
                    station_forecast.date_time_forecast,
                    station_forecast.station_id,
                )
            if exist is False:
                db.add(db_station_forecast)
                print(
                    f"add: {station_forecast.station_id}, {station_forecast.date_time_forecast}"
                )
                print(
                    "vdr = ",
                    vdr_dataframe_by_date.get(vdr_rdn["date"])["data_frame"][i],
                )
                print(
                    "rdn = ",
                    rdn_dataframe_by_date.get(vdr_rdn["date"])["data_frame"][i],
                )
            else:
                # todo add update method

                db.query(ModelStationsForecast).filter(
                    and_(
                        ModelStationsForecast.date_time_forecast == station_forecast.date_time_forecast,
                        ModelStationsForecast.station_id == station_forecast.station_id,
                    )
                ).update({"vdr": station_forecast.vdr})


                print(
                    f"update: {station_forecast.station_id}, {station_forecast.date_time_forecast}"
                )
                print(
                    f"is exist: {station_forecast.station_id}, {station_forecast.date_time_forecast}"
                )
        db.commit()
    db.close()
