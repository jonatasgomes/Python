import oracledb
import Database.env as env

class OracleDBConnectionFactory:
  def __init__(self):
    self.user = env.USER
    self.password = env.PASSWORD
    self.dsn = env.DSN

  def __enter__(self):
    self.connection = oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)
    return self.connection

  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.connection:
      self.connection.close()

def get_ndx_stocks():
  with OracleDBConnectionFactory() as connection:
    cursor = connection.cursor()
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
  with OracleDBConnectionFactory() as connection:
    cursor = connection.cursor()
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
    connection.commit()
