import os
import pandas as pd
import math
from gpxcsv import gpxtolist
from src.bcolors import bcolors
from src.bar_plot import bar_plot

def import_and_archive(gpx_file, db_client):
  print(f"Processing {bcolors.BOLD}{gpx_file}{bcolors.ENDC}:")
  df = pd.DataFrame(gpxtolist(gpx_file))

  # Format columns
  df = df[df['hr'].notna()]
  df.drop(columns=["name", "DisplayColor"], inplace=True)
  df["time"] = pd.to_datetime(df["time"], yearfirst=True, utc=False)

  # Get median of Date
  track_time = df["time"].quantile(0.5, interpolation="midpoint")
  print(f"... Median time: {track_time}")

  # Calculate HR ranges
  birthday = pd.Timestamp(1987,9,7)
  timedelta = (track_time.tz_convert(tz="UTC") - birthday.tz_localize(tz="UTC"))
  age = math.floor(timedelta.days / 365.25)
  estimated_max_hr = 220 - age
  cardio_low = math.floor(estimated_max_hr * 0.6)
  aerobic_low = math.floor(estimated_max_hr * 0.7)
  aerobic_high = math.floor(estimated_max_hr * 0.8)
  anaerobic_high = math.floor(estimated_max_hr * 0.9)

  # Evaluate HR ranges
  cardio_time = 0
  aerobic_time = 0
  anaerobic_time = 0
  vo2max_time = 0

  for i in range(1, df.shape[0] - 1):
      if df.iloc[i-1]["hr"] >= cardio_low and df.iloc[i]["hr"] >= cardio_low and df.iloc[i+1]["hr"] >= cardio_low:
          duration1 = (df.iloc[i]["time"] - df.iloc[i-1]["time"]).seconds / 2
          duration2 = (df.iloc[i+1]["time"] - df.iloc[i]["time"]).seconds / 2
          duration = duration1 + duration2
          if duration <= 60:
              if df.iloc[i]["hr"] < aerobic_low:
                cardio_time += duration
              elif df.iloc[i]["hr"] <= aerobic_high:
                aerobic_time += duration
              elif df.iloc[i]["hr"] <= anaerobic_high:
                anaerobic_time += duration
              else:
                vo2max_time += duration
  overall_time = cardio_time + aerobic_time + anaerobic_time + vo2max_time
  
  print("... Heart rate zones:")
  print(f"... {bcolors.OKBLUE}Cardio    60%-70%: {cardio_low} - {aerobic_low} bpm -> {round(cardio_time/60,2)} min {round(cardio_time / overall_time * 100, 1)}%{bcolors.ENDC}")
  print(f"... {bcolors.OKGREEN}Aerobic   70%-80%: {aerobic_low} - {aerobic_high} bpm -> {round(aerobic_time/60,2)} min {round(aerobic_time / overall_time * 100, 1)}%{bcolors.ENDC}")
  print(f"... {bcolors.WARNING}Anaerobic 80%-90%: {aerobic_high} - {anaerobic_high} bpm -> {round(anaerobic_time/60,2)} min {round(anaerobic_time / overall_time * 100, 1)}%{bcolors.ENDC}")
  print(f"... {bcolors.FAIL}VO2_max  90%-100%: {anaerobic_high} - {estimated_max_hr} bpm -> {round(vo2max_time/60,2)} min {round(vo2max_time / overall_time * 100, 1)}%{bcolors.ENDC}")
  print("... ", end="", sep="")
  bar_plot(52, [[cardio_time, bcolors.OKBLUE], [aerobic_time, bcolors.OKGREEN], [anaerobic_time, bcolors.WARNING], [vo2max_time, bcolors.FAIL]])

  json_body = [
    {
      "measurement": "endurance",
      "time": track_time,
      "fields": {
        "cardio": cardio_time,
        "aerobic": aerobic_time,
        "anaerobic": anaerobic_time,
        "vo2max": vo2max_time
      }
    }
  ]

  write_success = db_client.write_points(json_body, time_precision='ms')
  print(f"... Successfully written into influxDB: {write_success}")

  # Archive .gpx
  if write_success:
    archive_directory = os.path.join(os.path.dirname(gpx_file), "archive")
    if not os.path.exists(archive_directory):
      os.mkdir(archive_directory)
    os.rename(gpx_file, os.path.join(archive_directory, os.path.basename(gpx_file)))
    print(f"... Moved {os.path.basename(gpx_file)} to {archive_directory}")

  print()