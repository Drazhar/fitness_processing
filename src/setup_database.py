from influxdb import InfluxDBClient


def setup_database(client: InfluxDBClient,
                   database_name: str):
  client_contains_database = any(
      db["name"] == database_name for db in client.get_list_database())
  if not client_contains_database:
    client.create_database(database_name)
  client.switch_database(database_name)
