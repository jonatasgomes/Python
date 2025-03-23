from snowflake.snowpark import Session # type: ignore
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import env

session = Session.builder.configs(
  {
    "user": env.USER,
    "password": env.PASSWORD,
    "account": env.ACCOUNT,
    "warehouse": env.WAREHOUSE,
    "database": env.DATABASE,
    "schema": env.SCHEMA
}
).create()

sns.set_style("darkgrid")
matplotlib.rcParams["font.size"] = 14
matplotlib.rcParams["figure.figsize"] = (9, 5)
matplotlib.rcParams["figure.facecolor"] = "#00000000"

df_table = session.table("HISTORICAL_PRICES")
df_table.show()
