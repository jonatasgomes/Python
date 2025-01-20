import oracledb
import Database.env as env

_connection = None

def connect_to_db():
  global _connection
  _connection = oracledb.connect(user=env.USER, password=env.PASSWORD, dsn=env.DSN, tcp_connect_timeout=160, expire_time=4, retry_count=6, retry_delay=5)
  print('Connection created.')

def close_db_connection():
  global _connection
  if _connection:
    _connection.close()
    _connection = None
    print('Connection closed.')

def get_ndx_stocks():
  global _connection
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  cursor.execute(
    """
      select s.ticker, s.id, i.weight
        from st1_stocks s, st1_index_stocks i
      where i.index_id = 1
        and s.id = i.stock_id
      order by i.weight desc
    """
  )
  result = cursor.fetchall()
  if result:
    return [{'ticker': row[0], 'id': row[1], 'weight': row[2]} for row in result]
  return None

def save_stock_prices(stock_id, data, timeframe):
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  for index, row in data.iterrows():
    cursor.execute(
      """
        merge into st1_stock_prices sp
        using dual
            on (
                sp.stock_id = :stock_id
                and sp.price_dt = to_date(:price_dt, 'YYYY-MM-DD HH24:MI:SS')
                and sp.timeframe = :timeframe
              )
          when not matched then
            insert (
              stock_id, price_dt, timeframe, open, low, high, close, volume
            ) values (
              :stock_id, to_date(:price_dt, 'YYYY-MM-DD HH24:MI:SS'), :timeframe, :open, :low, :high, :close, :volume
            )
      """,
      stock_id=stock_id,
      price_dt=index.strftime('%Y-%m-%d %H:%M:%S'),
      timeframe=timeframe,
      open=row['Open'],
      low=row['Low'],
      high=row['High'],
      close=row['Close'],
      volume=row['Volume']
    )
  _connection.commit()
