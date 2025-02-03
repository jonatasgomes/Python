import oracledb
import data.env as env

_connection = None

def connect_to_db():
  global _connection
  _connection = oracledb.connect(user=env.ORACLE_USER, password=env.ORACLE_PASSWORD, dsn=env.ORACLE_DSN, tcp_connect_timeout=160, expire_time=4, retry_count=6, retry_delay=5)
  print('Connection created.')

def close_db_connection():
  global _connection
  if _connection:
    _connection.close()
    _connection = None
    print('Connection closed.')

def execute_sql_query(sql_query):
    try:
      connect_to_db()
      cursor = _connection.cursor()
      cursor.execute(sql_query)
      results = cursor.fetchall()
      close_db_connection()
      if not results:
        return 'No data found.'
      return results
    except Exception as e:
      return f'Database error: {str(e)}'
