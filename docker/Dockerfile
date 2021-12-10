FROM python:3

WORKDIR /usr/local/bin/
RUN pip install influxdb
COPY influx_client .
RUN chmod +x influx_client