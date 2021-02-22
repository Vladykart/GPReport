from gpreport.upload_reports import fetch_and_upload_rdn_for_tomorrow, pre_uploader
from datetime import datetime as dt

#!/usr/bin/env python

# python script which needs an environment variable and runs as a cron job
import datetime
import os

import schedule
import time

# print("Script has been started at {}".format(datetime.strftime(datetime.today(), "%d.%m.%Y")))


def job():
    print("I'm working...")
    fetch_and_upload_rdn_for_tomorrow(
        path="./StationCoordinates.csv",
        date_from=dt.strftime(dt.today(), "%d.%m.%Y"),
        num_date_range=1,
    )

def job_2():
    print("I'm working...")
    pre_uploader(
        path="./StationCoordinates.csv",
        date_from=dt.strftime(dt.today(), "%d.%m.%Y"),
        num_date_range=1,)


job()
schedule.every(1).day.at("09:16").do(job)
schedule.every(2).hours.do(job_2)
# schedule.every().hour.do(job_2)

while True:
    schedule.run_pending()
    print("I'm working...")
    time.sleep(1)
