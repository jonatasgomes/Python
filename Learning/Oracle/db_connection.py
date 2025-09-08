import oracledb
from dotenv import dotenv_values

env = dotenv_values()
print(env)

with oracledb.connect(user=env['user'], password=env['pwd'], dsn=f'{env["dns"]}:{env["port"]}/{env["sid"]}') as connection:
  with connection.cursor() as cursor:
    cursor.execute('SELECT table_name FROM user_tables')
    for row in cursor:
      print(row)
