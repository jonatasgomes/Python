import sqlite3
import pandas as pd

conn = sqlite3.connect('web.db')
df_data = pd.read_csv('random_data.csv', index_col=0)
df_data.index.name = 'index_name'
# df_data.to_sql('data', conn, index_label='index_name')

c = conn.cursor()
# c.execute('drop table products')
# c.execute('create table products (product_id INTEGER PRIMARY KEY, product_name TEXT, price INTEGER)')
# c.execute('''INSERT INTO products (product_id, product_name, price)
#     VALUES
#     (1, 'Computer', 800),
#     (2, 'Printer', 200),
#     (3, 'Tablet', 300)
# ''')
# conn.commit()

# c.execute('update products set price = price * 2')
# conn.commit()
df = pd.read_sql('select * from products where price > 200', conn)
print(df)
conn.close()
