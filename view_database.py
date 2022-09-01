from src.get_db_client import get_db_client


db_client = get_db_client()

db_client.switch_database("training")
print(db_client.get_list_series())
results = db_client.query("SHOW FIELD KEYS")
for point in results.get_points():
  print(point)

results = db_client.query('SELECT * FROM "endurance"')
for point in results.get_points():
  print(point)

db_client.close()
