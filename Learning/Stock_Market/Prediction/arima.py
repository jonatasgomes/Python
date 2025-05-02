import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Function to train the ARIMA model and make a prediction
def predict_close_price(train_data, open_price):
    model = ARIMA(train_data['CLOSE'], order=(1, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=1)
    predicted_close = forecast.predicted_mean.iloc[0]

    # Incorporate today's open price (you might want to refine this)
    # For now, let's simply average the prediction with the open price
    final_prediction = (predicted_close + open_price) / 2
    return final_prediction

# Streamlit app
def main():
    st.title('Stock Closing Price Prediction App')

    # File uploader
    uploaded_file = st.file_uploader('Upload CSV file with historical stock data', type='csv')

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df['DT'] = pd.to_datetime(df['DT'])
            df = df.set_index('DT')

            st.subheader('Historical Data')
            st.dataframe(df.head())

            # Open price input
            open_price = st.number_input("Enter today's opening price", value=0.0)

            if open_price > 0:
                # Train model and make prediction
                predicted_close = predict_close_price(df, open_price)
                st.success(f'Predicted Closing Price: {predicted_close:.2f}')

                # Optional: Plot historical data
                st.subheader('Historical Closing Prices')
                st.line_chart(df['CLOSE'])

        except Exception as e:
            st.error(f'An error occurred: {e}')

if __name__ == "__main__":
    main()