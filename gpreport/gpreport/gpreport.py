"""Main module."""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from time import sleep
from typing import List
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class GPReport(ABC):
    """Abstract Class defines a template method containing the skeleton of some
    an algorithm (usually) consisting of calls to abstract primitive operations.
    Concrete subclasses should implement these operations, but leave themselves
    template method unchanged."""

    # TODO: add SSL support !!!
    def __init__(self, login, password, station_id, date, collector):
        self.login = login
        self.password = password
        self.date = date
        self.objs_req = station_id
        self.collector = collector
        self.login_url = "https://www.gpee.com.ua/login/try"
        self.headers = None
        self.payload = None
        self.send_date_url = None
        self.soup = None
        self.ingredients = None
        self.table_body = None
        self.data = None
        self.rows = None
        self.new_request_url = None
        self.table = None
        self.records = None
        self.vdr_data = None

    def template_method_rdn(self):
        """The template method defines the skeleton of algorithm."""
        self.create_config()  # required_operations
        self.create_payload()  # required_operations
        self.create_headers()  # required_operations
        self.do_login()
        sleep(2)  # base operations
        self.send_date()
        sleep(2)  # base operations
        self.send_new_request()  # base operations
        self.make_soup()  # base operations
        self.find_table()  # base oper-ations
        self.find_rows()  # base operations
        return self.find_yummy_data()  # base operations

    def do_login(self):
        requests.post(url=self.login_url, headers=self.headers, data=self.payload)

    def send_date(self):
        self.ingredients = requests.post(
            url=self.send_date_url, headers=self.headers, data={"date": self.date}
        )

    def send_new_request(self):
        self.ingredients = requests.post(
            url=self.new_request_url,
            headers=self.headers,
            data={"date_req": str(self.date), "objs_req": self.objs_req},
        )

    def make_soup(self):
        self.soup = BeautifulSoup(self.ingredients.text, "html.parser")

    def find_table(self):
        table = self.soup.find(attrs={"class": self.table})
        self.table_body = table.find("tbody")

    def find_rows(self):
        self.rows = self.table_body.find_all("tr")

    def fetch_vdr_menu_table_data(self):
        data = []
        for row in self.rows:
            col = row.find_all("td")
            data.append(
                {
                    "station_id": row.find("td", attrs={"class": "STATION_ID"}).text,
                    "ml_id": row.find("td", attrs={"class": "ml_id"}).text,
                    "status": col[5].text,
                    "date": col[4].text,
                    "name": col[3].text,
                }
            )
        self.records = data

    def find_yummy_data(self):
        data = []
        if self.rows:
            for row in self.rows:
                col = row.find_all("td")
                time = col[0].text.strip()
                value_1 = col[1].text.strip()
                value_2 = col[2].text.strip()
                data.append({"time": time, "value_1": value_1, "value_2": value_2})
            return data

    def fetch_data_from_records(self):
        if self.records:
            for record in tqdm(self.records):
                data = {
                    "date_req_vdr": record["date"],
                    "objs_req_vdr": record["station_id"],
                    "ml_id": record["ml_id"],
                }
                self.ingredients = requests.post(
                    url=self.new_request_url, headers=self.headers, data=data
                )
                sleep(1)
                try:
                    self.make_soup()
                    self.find_table()
                    self.find_rows()
                    self.collector.append(self.find_yummy_data())
                except AttributeError:
                    pass

    @abstractmethod
    def create_config(self):
        raise NotImplementedError()

    @abstractmethod
    def create_payload(self):
        raise NotImplementedError()

    @abstractmethod
    def create_headers(self):
        raise NotImplementedError()


class GPReportRDN(GPReport):
    def create_config(self):
        self.send_date_url = "https://www.gpee.com.ua/maket_rdn/send_date"
        self.new_request_url = "https://www.gpee.com.ua/maket_rdn/new_request"
        self.table = "col-xs-6"

    def create_payload(self):
        self.payload = (
            "login=" + str(self.login) + "&password=" + str(self.password) + ""
        )

    def create_headers(self):
        self.headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.`7  7,uk;q=0.6",
            "Cookie": "PHPSESSID=tml5c76k5vesvt3s5j5duldpb1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }


class GPReportVDR(GPReport):
    def template_method_vdr(self):

        self.create_config()  # required_operations
        self.create_payload()  # required_operations
        self.create_headers()  # required_operations
        self.do_login()
        sleep(2)
        self.send_date()
        sleep(2)
        self.make_soup()
        self.find_table()
        self.find_rows()
        self.fetch_vdr_menu_table_data()
        self.fetch_data_from_records()
        return self.collector

    def create_payload(self):
        self.payload = (
            "login=" + str(self.login) + "&password=" + str(self.password) + ""
        )

    def create_headers(self):
        self.headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.`7  7,uk;q=0.6",
            "Cookie": "PHPSESSID=tml5c76k5vesvt3s5j5duldpb1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    def create_config(self):
        self.send_date_url = "https://www.gpee.com.ua/index.php/maket_vdr/send_date_vdr"
        self.new_request_url = (
            "https://www.gpee.com.ua/index.php/maket_vdr/new_request_vdr"
        )
        self.table = "system-table"


def get_date_range(date=datetime.today(), date_range=1):
    base = date
    num_days = date_range
    date_list = [base.date() - timedelta(days=x) for x in range(num_days)]
    date_list = [date.strftime("%d-%m-%Y") for date in date_list]
    return date_list


def get_garpok_rdn(login, password, station_id, date):
    collector = []
    rdn = GPReportRDN(
        login=login,
        password=password,
        date=date,
        station_id=station_id,
        collector=collector,
    )
    rdn.template_method_rdn()
    return collector


def get_garpok_vdr(login, password, station_id, date):
    collector = []
    vdr = GPReportVDR(
        login=login,
        password=password,
        date=date,
        station_id=station_id,
        collector=collector,
    )
    vdr.template_method_vdr()
    print(collector)
    return collector


def preparate_data_from_vdr(df):
    df = df[["time", "value_1"]]
    df = df.reset_index()
    df = df[df["time"] != "25"]
    df.loc[df.time == "24", "time"] = "00"
    df = df.reindex(index=df.index[::-1])
    df["time"] = pd.to_datetime(df["time"], format="%H", errors="coerce").dt.time
    df["idx"] = df.groupby("time").cumcount()
    df = df.pivot(index="time", columns="idx")[["value_1"]]
    df = df.replace(r"^\s*$", np.nan, regex=True)
    df["value_1"] = df["value_1"].astype("float32") * 1000
    df["result"] = df.ffill(1).iloc[:, -1]
    df = df.reset_index()
    df = df.apply(lambda x: sorted(x, key=pd.notnull), 0)
    return df


def get_records_by_stations(stations, date):
    return


def get_records_by_date_range(date_list: List):
    return
