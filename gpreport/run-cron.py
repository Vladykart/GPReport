#!/usr/bin/env python

# run-cron.py
# sets environment variable crontab fragments and runs cron

import os
from subprocess import call
import fileinput

# read docker environment variables and set them in the appropriate crontab fragment
environment_variable = os.environ["dev"]

for line in fileinput.input("/etc/cron.d/RUN pip install -r requirements.txt",inplace=1):
    print(line.replace("XXXXXXX", environment_variable))

args = ["cron", "-f", "-L 15"]
call(args)
