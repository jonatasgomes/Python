import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Asimov Master Class", page_icon=":books:")
st.write("Book Reviews")

df_top100_books = pd.read_csv("./datasets/Top-100 Trending Books.csv")
df_reviews = pd.read_csv("./datasets/customer reviews.csv")

books = sorted(df_top100_books["book title"].unique())
book = st.sidebar.selectbox("Books", books)

df_book = df_top100_books[df_top100_books["book title"] == book]
df_book_reviews = df_reviews[df_reviews["book name"] == book]
book_title = df_book["book title"].values[0]
book_genre = df_book["genre"].values[0]
book_price = f"${df_book['book price'].values[0]}"
book_rating = df_book["rating"].values[0]
book_year = df_book["year of publication"].values[0]

st.title(book_title)
st.subheader(book_genre)
col1, col2, col3 = st.columns(3)
col1.metric("Price", book_price)
col2.metric("Rating", book_rating)
col3.metric("Year of Publication", book_year)
st.divider()
for row in df_book_reviews.values:
    message = st.chat_message(str(row[4]))
    message.write(f"**{row[2]}**")
    message.write(row[5])
