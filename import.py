#!/usr/bin/env python
import os
import re
from influxdb import InfluxDBClient
from src.setup_database import setup_database
from src.gpx import import_and_archive
from src.libra_weight import import_and_delete

db_client = InfluxDBClient(host='192.168.0.2', port=8086, username='admin', password='B9CCujOBCY')
setup_database(db_client, "training")
#client.drop_measurement("endurance")
#client.alter_retention_policy("autogen",duration="INF")

gpx_directory = "."
for filename in os.listdir(gpx_directory):
  if filename.endswith(".gpx"):
    gpx_file = os.path.join(gpx_directory, filename)
    import_and_archive(gpx_file, db_client)

libra_csv_dir = "/home/drazhar/Dropbox/Eigene Sachen/"
for filename in os.listdir(libra_csv_dir):
  if re.search("Libra.*\.csv",filename,flags=re.IGNORECASE):
    csv_file = os.path.join(libra_csv_dir, filename)
    import_and_delete(csv_file, db_client)

db_client.close()