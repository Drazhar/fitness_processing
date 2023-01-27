#!./.venv/bin/python3
import os
import re
from src.setup_database import setup_database
from src.gpx import import_and_archive
from src.libra_weight import import_and_delete
from src.get_db_client import get_db_client


db_client = get_db_client()

setup_database(db_client, "training")

gpx_directory = "."
for filename in os.listdir(gpx_directory):
  if filename.endswith(".gpx"):
    gpx_file = os.path.join(gpx_directory, filename)
    import_and_archive(gpx_file, db_client)

libra_csv_dir = "/home/traphi/Dropbox/Eigene Sachen"
for filename in os.listdir(libra_csv_dir):
  if re.search("Libra.*\.csv",filename,flags=re.IGNORECASE):
    csv_file = os.path.join(libra_csv_dir, filename)
    import_and_delete(csv_file, db_client)

db_client.close()
