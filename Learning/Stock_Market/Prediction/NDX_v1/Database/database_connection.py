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
  return [{'ticker': row[0], 'id': row[1], 'weight': row[2]} for row in result] if result else None

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

def get_train_data_base():
  global _connection
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  cursor.execute(
    """
      select p.price_dt, s.ticker, p.open as price_0930,
            (
              select p1.open
                from st1_stock_prices p1
                where p1.stock_id = p.stock_id
                  and p1.price_dt = p.price_dt + 11.5/24
                  and p1.timeframe = '30m'
            ) as price_1130
        from st1_stock_prices p, st1_stocks s
      where s.id <> 1
        and p.stock_id = s.id
        and p.timeframe = '1d'
        and p.price_dt < trunc(sysdate)
      order by 1
    """
  )
  result = cursor.fetchall()
  return [{'price_dt': row[0], 'ticker': row[1], 'price_0930': row[2], 'price_1130': row[3]} for row in result] if result else None

def get_train_data_ndx():
  global _connection
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  cursor.execute(
    """
      select p.price_dt, p.open as spx_price_0930,
            (
              select p1.open
                from st1_stock_prices p1
                where p1.stock_id = p.stock_id
                  and p1.price_dt = p.price_dt + 11.5/24
                  and p1.timeframe = '30m'
            ) as spx_price_1130,
            p.low as spx_price_low, p.high as spx_price_high
        from st1_stock_prices p, st1_stocks s
      where s.id = 1
        and p.stock_id = s.id
        and p.timeframe = '1d'
      order by 1
    """
  )
  result = cursor.fetchall()
  return [{'price_dt': row[0], 'spx_price_0930': row[1], 'spx_price_1130': row[2], 'spx_price_low': row[3], 'spx_price_high': row[4]} for row in result] if result else None

def get_predict_data_base():
  global _connection
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  cursor.execute(
    """
      select p.price_dt, s.ticker, p.open as price_0930,
            (
              select p1.open
                from st1_stock_prices p1
                where p1.stock_id = p.stock_id
                  and p1.price_dt = p.price_dt
                  and p1.timeframe = '30m'
            ) as price_1130
        from st1_stock_prices p, st1_stocks s
      where s.id <> 1
        and p.stock_id = s.id
        and p.timeframe = '30m'
        and p.price_dt >= trunc(sysdate)
      order by 1
    """
  )
  result = cursor.fetchall()
  return [{'price_dt': row[0], 'ticker': row[1], 'price_0930': row[2], 'price_1130': row[3]} for row in result] if result else None

def get_predict_data_ndx():
  global _connection
  if _connection is None:
    raise Exception('Connection not created.')
  cursor = _connection.cursor()
  cursor.execute(
    """
      select p.price_dt, p.open as spx_price_0930,
            (
              select p1.open
                from st1_stock_prices p1
                where p1.stock_id = p.stock_id
                  and p1.price_dt = p.price_dt
                  and p1.timeframe = '30m'
            ) as spx_price_1130
        from st1_stock_prices p, st1_stocks s
      where s.id = 1
        and p.stock_id = s.id
        and p.timeframe = '30m'
        and p.price_dt >= trunc(sysdate)
      order by 1
    """
  )
  result = cursor.fetchall()
  return [{'price_dt': row[0], 'spx_price_0930': row[1], 'spx_price_1130': row[2]} for row in result] if result else None
