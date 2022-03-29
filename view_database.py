from influxdb import InfluxDBClient
db_client = InfluxDBClient(host='192.168.0.2', port=8086, username='admin', password='B9CCujOBCY')

db_client.switch_database("training")
print(db_client.get_list_series())
results = db_client.query("SHOW FIELD KEYS")
for point in results.get_points():
  print(point)

results = db_client.query('SELECT * FROM "endurance"')
for point in results.get_points():
  print(point)

db_client.close()