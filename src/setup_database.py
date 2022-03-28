def setup_database(client,database_name):
  client_contains_database = False
  for db in client.get_list_database():
    if db["name"] == database_name:
      client_contains_database = True
      break
  if not client_contains_database:
    client.create_database(database_name)
  client.switch_database(database_name)