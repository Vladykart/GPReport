from datetime import datetime, timedelta
from pprint import pprint
import pandas as pd

from gpreport import gpreport as gp
from database import (
    create_station_forecast,
    check_forecast_is_exists,
    write_rdn_for_tomorrow,
)
from schemas import StationsForecast as SchemaStationsForecast


def read_station_info(path):
    exclude = [
        65,
        93,
        97,
        98,
        99,
        101,
        102,
        103,
        104,
        121,
        122,
        129,
        130,
        154,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        168,
        169,
        170,
        171,
        172,
        173,
        174,
        175,
        176,
        180,
        181,
        182,
        183,
        184,
        185,
    ]
    df = pd.read_csv(path)
    df = df[df["gpnumber"] != 0]
    df = df[df["id_st"].isin(exclude) != True]

    return df[["id_st", "gpnumber", "GarpokLogin", "GarpokPassword"]].to_dict(
        orient="index"
    )


def get_date_range(date_from, num_date_range=1):
    base = datetime.strptime(date_from, "%d.%m.%Y")
    num_days = num_date_range
    date_list = [base.date() - timedelta(days=x) for x in range(num_days)]
    return [date.strftime("%d-%m-%Y") for date in date_list]


def fetch_forecasts_by_stations(login, password, station_id, date_list):

    vdr_dataframes = gp.get_vdr_dataframes(
        login, password, station_id, date_list=date_list
    )
    rdn_dataframes = gp.get_rdn_dataframes(
        login, password, station_id, date_list=date_list
    )
    return vdr_dataframes, rdn_dataframes


def get_unique_numbers(dates):
    list_of_unique_dates = []
    unique_numbers = set(dates)
    for number in unique_numbers:
        list_of_unique_dates.append(number)
    print(list_of_unique_dates)
    return list_of_unique_dates


def pre_uploader(
    path: str,
    date_from: datetime = datetime.strftime(
        datetime.today() - timedelta(days=1), "%d.%m.%Y"
    ),
    num_date_range: int = 1,
):
    stations_info_list = read_station_info(path)
    date_list = get_date_range(date_from, num_date_range)
    c = len(stations_info_list)
    for station in stations_info_list.values():
        c -= 1
        print(c)
        dates_for_forecast = []
        date_forecast = None
        data = []
        for date in date_list:
            for i in range(24):
                d = datetime.combine(
                    datetime.strptime(str(date), "%d-%m-%Y").date(),
                    datetime.strptime(str(i), "%H").time(),
                )
                if check_forecast_is_exists(d, station["id_st"]) is False:
                    dates_for_forecast.append(date)
                    date_forecast = date
                else:
                    dates_for_forecast.append(date)
                    date_forecast = date


        if get_unique_numbers(dates_for_forecast):
            print(f'fetch {station["id_st"]}')
            try:
                daily_vdr, daily_rdn = fetch_forecasts_by_stations(
                    login=str(station["GarpokLogin"]),
                    password=str(station["GarpokPassword"]),
                    station_id=str(station["gpnumber"]),
                    date_list=get_unique_numbers(dates_for_forecast),
                )
                data.append({"vdr": daily_vdr, "rdn": daily_rdn, "date": date_forecast})
            except TypeError:
                print(f'data is not found for station {station["id_st"]}')
                continue

        else:
            print(f'{station["id_st"]} is exist passed')

        create_station_forecast(data=data, station_id=station["id_st"])


def fetch_and_upload_rdn_for_tomorrow(
    path: str,
    date_from: datetime = datetime.strftime(
        datetime.today() + timedelta(days=1), "%d.%m.%Y"
    ),
    num_date_range: int = 1,
):
    stations_info_list = read_station_info(path)
    date_list = get_date_range(date_from, num_date_range)
    for station in stations_info_list.values():
        dates_for_forecast = []

        data = []
        for date in date_list:
            for i in range(24):
                d = datetime.combine(
                    datetime.strptime(str(date), "%d-%m-%Y").date(),
                    datetime.strptime(str(i), "%H").time(),
                )
                if check_forecast_is_exists(d, station["id_st"]) is False:
                    dates_for_forecast.append(date)
                else:
                    print(f'{station["id_st"]}, {d} is exist passed')

            if get_unique_numbers(dates_for_forecast):
                print(f'fetch {station["id_st"]}')
                try:
                    data.append(
                        gp.get_rdn_dataframes(
                            login=str(station["GarpokLogin"]),
                            password=str(station["GarpokPassword"]),
                            station_id=str(station["gpnumber"]),
                            date_list=get_unique_numbers(dates_for_forecast),
                        )
                    )
                except TypeError:
                    print(f'RDN data is not found for station {station["id_st"]}')
                    continue
            else:
                print(f'{station["id_st"]} is exist passed')

            write_rdn_for_tomorrow(data=data, station_id=station["id_st"])


# if __name__ == "__main__":
#     fetch_and_upload_rdn_for_tomorrow(
#         path="../StationCoordinates.csv",
#         date_from=datetime.strftime(datetime.today(), "%d.%m.%Y"),
#         num_date_range=1
#     )
