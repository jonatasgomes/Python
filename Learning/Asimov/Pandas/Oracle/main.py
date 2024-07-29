import os
import cx_Oracle
from sqlalchemy import create_engine
import pandas as pd

lib_dir = os.environ.get("LD_LIBRARY_PATH")
cx_Oracle.init_oracle_client(lib_dir=lib_dir)

engine = create_engine('oracle://ifj:cj$2024@cjt-km-dev.ccvxbrbziyuz.ca-central-1.rds.amazonaws.com:1521/devcgo')
df = pd.DataFrame(data={'col1': [1, 2, 3], 'col2': [2, 4, 6]})
df.to_sql('temp_pandas', con=engine, if_exists='replace', index=False)
