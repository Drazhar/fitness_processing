import os
import pandas as pd
import plotext as plt
from src.bcolors import bcolors

def import_and_delete(csv_file, db_client):
  print(f"Processing {bcolors.BOLD}{csv_file}{bcolors.ENDC}:")
  df = pd.read_csv(csv_file, sep=";", skiprows=2)
  df.rename(columns={"#date":"date"}, inplace=True)
  df["date"] = pd.to_datetime(df["date"], yearfirst=True, utc=False)

  json_body = []
  x = []
  y = []
  for i in range(0, df.shape[0]):
    x.append((df.iloc[i]["date"] - pd.Timestamp.now()).days)
    y.append(df.iloc[i]["weight"])
    json_body.append({
      "measurement": "body",
      "time": f"{df.iloc[i]['date'].date()}T12:00:00Z",
      "fields": {
        "weight": df.iloc[i]["weight"],
      }
    })

  plt.plot(x,y)
  plt.plot_size(80,10)
  plt.frame(False)
  plt.colorless()
  plt.show()

  write_success = db_client.write_points(json_body, time_precision='ms')
  print(f"... Successfully written into influxDB: {write_success}")

  if write_success:
    os.remove(csv_file)
    print(f"... {os.path.basename(csv_file)} deleted")
  print()