import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient


def get_db_client() -> InfluxDBClient:
    load_dotenv()
    return InfluxDBClient(host     = os.getenv("INFLUX_IP"),
                          port     = os.getenv("INFLUX_PORT"),
                          username = os.getenv("INFLUX_USER"),
                          password = os.getenv("INFLUX_PASS"))
