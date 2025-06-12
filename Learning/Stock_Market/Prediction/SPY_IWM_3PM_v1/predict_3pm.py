import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_intraday_data(ticker, period='7d', interval='1m'):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)
    df = df.tz_convert('US/Eastern') # Align to NY time
    return df

iwm = get_intraday_data("IWM")
spy = get_intraday_data("SPY")

def extract_features(df):
    # flatten MultiIndex columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    df = df.between_time("09:30", "16:00")
    feature_rows = []
    target_rows = []
    for date in df.index.normalize().unique():
        day_df = df[df.index.normalize() == date]
        if len(day_df) == 0: continue
        try:
            row_3pm = day_df.between_time("15:00", "15:00").iloc[0]
            row_4pm = day_df.between_time("15:59", "15:59").iloc[0]
            # If you get a DataFrame/Series on Close, use .iloc[0]
            close_3pm = row_3pm['Close'].iloc[0] if isinstance(row_3pm['Close'], pd.Series) else row_3pm['Close']
            close_4pm = row_4pm['Close'].iloc[0] if isinstance(row_4pm['Close'], pd.Series) else row_4pm['Close']
            close_5m_ago = day_df.loc[:row_3pm.name - pd.Timedelta(minutes=5)]['Close'].iloc[-1]
            close_15m_ago = day_df.loc[:row_3pm.name - pd.Timedelta(minutes=15)]['Close'].iloc[-1]
            temp_df = day_df.loc[:row_3pm.name]
            vwap = (temp_df['Close'] * temp_df['Volume']).sum() / temp_df['Volume'].sum()
        except Exception as e:
            continue
        f = {
            'close': close_3pm,
            'return_5m': (close_3pm - close_5m_ago)/close_5m_ago,
            'return_15m': (close_3pm - close_15m_ago)/close_15m_ago,
            'vwap_diff': (close_3pm - vwap)/vwap,
            'volume': row_3pm['Volume'].iloc[0] if isinstance(row_3pm['Volume'], pd.Series) else row_3pm['Volume'],
        }
        feature_rows.append(f)
        target_rows.append(int(close_4pm > close_3pm))
    return pd.DataFrame(feature_rows), pd.Series(target_rows)

iwm_X, iwm_y = extract_features(iwm)
spy_X, spy_y = extract_features(spy)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(iwm_X, iwm_y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

def live_predict(name, df, clf, target_time="15:00"):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    df = df.between_time("09:30", "16:00")
    today = df.index.normalize()[-1]
    day_df = df[df.index.normalize() == today]
    try:
        row_3pm = day_df.between_time(target_time, target_time).iloc[0]
        close_3pm = row_3pm['Close']
        close_5m_ago = day_df.loc[:row_3pm.name - pd.Timedelta(minutes=5)]['Close'].iloc[-1]
        close_15m_ago = day_df.loc[:row_3pm.name - pd.Timedelta(minutes=15)]['Close'].iloc[-1]
        temp_df = day_df.loc[:row_3pm.name]
        vwap = (temp_df['Close'] * temp_df['Volume']).sum() / temp_df['Volume'].sum()
        volume3 = row_3pm['Volume']
    except Exception as e:
        print("Market not open or 3pm bar not available.", e)
        return

    f = {
        'close': close_3pm,
        'return_5m': (close_3pm - close_5m_ago)/close_5m_ago,
        'return_15m': (close_3pm - close_15m_ago)/close_15m_ago,
        'vwap_diff': (close_3pm - vwap)/vwap,
        'volume': volume3,
    }
    fx = pd.DataFrame([f])
    proba = clf.predict_proba(fx)[0]
    print(f"Probability {name} closes HIGHER at 4pm than 3pm: {proba[1]:.2f}", "UP" if proba[1]>0.5 else "DOWN")

live_predict('IWM', iwm, clf)
live_predict('SPY', spy, clf)
