# BUILD-USING:        docker build -t test-cron .
# RUN-USING docker run --detach=true --volumes-from t-logs --name t-cron test-cron


FROM python:3

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron postgresql-client
RUN touch /var/log/cron.log
RUN mkdir -p /usr/src/app/garpok/
WORKDIR /usr/src/app/garpok
COPY . gpreport /usr/src/app/garpok/
ADD . gpreport /usr/src/app/garpok/
#RUN pip3 install virtualenv
#RUN virtualenv  --python=python3 dev
#RUN virtualenv dev
#RUN source ./app/bin/activate
RUN pip install -r requirements.txt
EXPOSE 8000
COPY crontab /etc/cron.d/cjob
RUN chmod 0644 /etc/cron.d/cjob
ENV PYTHONUNBUFFERED 1
CMD ["python3", "main.py"]














##
## Set correct environment variables.
#ENV HOME /root
#ENV TEST_ENV test-value
#
#RUN apt-get update && apt-get install -y software-properties-common python-software-properties && apt-get update
#
## Install Python Setuptools
#RUN apt-get install -y python cron
#
#
#RUN apt-get purge -y python-software-properties software-properties-common && apt-get clean -y && apt-get autoclean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
#RUN pip install -r requirements.txt
#ADD RUN pip install -r requirements.txt /etc/cron.d/
#ADD test.py /
#ADD run-cron.py /
#
#RUN chmod a+x test.py run-cron.py
#
## Set the time zone to the local time zone
#RUN echo "Ukrain/Kiev" > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata
#
#CMD ["/run-cron.py"]
#
#EXPOSE 8000







#FROM python:3.8
#RUN mkdir -p /usr/src/app/garpok/
#WORKDIR /usr/src/app/garpok
#COPY . gpreport /usr/src/app/garpok/
#RUN pip install -r requirements.txt
#EXPOSE 8000
#CMD ["python3", "main.py"]
# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build



