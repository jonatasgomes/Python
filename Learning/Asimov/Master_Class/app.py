import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Asimov Master Class", page_icon=":books:")
df_reviews = pd.read_csv("./datasets/customer reviews.csv")
df_top100_books = pd.read_csv("./datasets/Top-100 Trending Books.csv")

price_max = df_top100_books["book price"].max()
price_min = df_top100_books["book price"].min()

price_range = st.sidebar.slider("Price Range", min_value=price_min, max_value=price_max, value=(price_min, price_max))
df_books = df_top100_books[df_top100_books["book price"].between(*price_range)]
bar = px.bar(df_books["year of publication"].value_counts().sort_index(), title="Number of Books Published by Year")
hist = px.histogram(df_books["book price"], title="Distribution of Book Prices")

col1, col2 = st.columns(2)
col1.plotly_chart(bar)
col2.plotly_chart(hist)
