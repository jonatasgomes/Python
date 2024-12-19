import oracledb
import os
from dotenv import dotenv_values

env = dotenv_values()

with oracledb.connect(user=env['user'], password=env['pwd'], dsn=f'{env["dns"]}:{env["port"]}/{env["sid"]}') as connection:
  with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM DUAL')
    for row in cursor:
      print(row)
