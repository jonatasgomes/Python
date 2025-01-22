import pandas as pd
import xgboost as xgb
import Database.database_connection as db

db.connect_to_db()
train_data_base = db.get_train_data_base()
train_data_ndx = db.get_train_data_ndx()
predict_data_base = db.get_predict_data_base()
predict_data_ndx = db.get_predict_data_ndx()
db.close_db_connection()

df = pd.DataFrame(train_data_base)
melted_df = pd.melt(
    df,
    id_vars=["price_dt", "ticker"],
    value_vars=["price_0930", "price_1130"],
    var_name="price_type",
    value_name="price"
)
melted_df["ticker_price_type"] = melted_df["ticker"] + "_" + melted_df["price_type"]
train_df = melted_df.pivot(
    index="price_dt",
    columns="ticker_price_type",
    values="price"
)
train_df.reset_index(inplace=True)

df_ndx = pd.DataFrame(train_data_ndx)
train_df = pd.merge(train_df, df_ndx, left_on="price_dt", right_on="price_dt", how="inner")
# print(train_df)

df = pd.DataFrame(predict_data_base)
melted_df = pd.melt(
    df,
    id_vars=["price_dt", "ticker"],
    value_vars=["price_0930", "price_1130"],
    var_name="price_type",
    value_name="price"
)
melted_df["ticker_price_type"] = melted_df["ticker"] + "_" + melted_df["price_type"]
predict_df = melted_df.pivot(
    index="price_dt",
    columns="ticker_price_type",
    values="price"
)
predict_df.reset_index(inplace=True)

df_ndx = pd.DataFrame(predict_data_ndx)
predict_df = pd.merge(predict_df, df_ndx, left_on="price_dt", right_on="price_dt", how="inner")
# print(predict_df)

# Prepare training data
X_train = train_df.drop(columns=["price_dt", "spx_price_low", "spx_price_high"])
y_train_low = train_df["spx_price_low"]
y_train_high = train_df["spx_price_high"]

# Train model for spx_low
model_low = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model_low.fit(X_train, y_train_low)

# Train model for spx_high
model_high = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model_high.fit(X_train, y_train_high)

# Prepare prediction data
X_predict = predict_df.drop(columns=["price_dt"])

# Predict spx_low and spx_high
predict_df["predicted_spx_price_low"] = model_low.predict(X_predict)
predict_df["predicted_spx_price_high"] = model_high.predict(X_predict)

print(predict_df[["price_dt", "predicted_spx_price_low", "predicted_spx_price_high"]])
