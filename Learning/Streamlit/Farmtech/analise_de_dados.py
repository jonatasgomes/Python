import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from data_generator import generate_data

st.set_page_config(
    page_title="Análise de Dados",
    page_icon=":bar_chart:",
    layout="wide"
)
st.title("Exploração de Dados")

st.header("1. Carregar os Dados")
df = generate_data()
st.subheader("Visualização de Dados")
st.dataframe(df.head(), use_container_width=True, hide_index=True)

st.header("2. Visualização de Dados")
st.subheader("Informações do Dataframe")
st.write("Dimensões do DataFrame:")
st.write(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
st.subheader("Tipos de Dados")
df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipos de Dados': df.dtypes.astype(str)
})
st.dataframe(df_types, hide_index=True)
st.subheader("Valores Ausentes")
st.write(df.isna().sum())
st.subheader("Estatísticas Descritivas")
st.write(df.describe())

st.header("3. Análise Univariada")
numeric_columns = ["Temperatura", "Precipitação", "Umidade", "Produção"]
categorical_columns = ["Fertilizante", "Tipo de Solo"]
st.subheader("Distribuições das Variáveis Numéricas")
for col in numeric_columns:
    # st.write(f"**{col}**")
    fig = px.histogram(df, x=col, nbins=30, title=f"Distribuição de {col}")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Box Plots das Variáveis Numéricas")
for col in numeric_columns:
    # st.write(f"**{col}**")
    fig = px.box(df, y=col, points="all", title=f"Box Plot de {col}")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Distribuições das Variáveis Categóricas")
for col in categorical_columns:
    # st.write(f"**{col}**")
    fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
    st.plotly_chart(fig, use_container_width=True)

st.header("4. Análise Bivariada")
st.subheader("Gráficos de Dispersão entre Variáveis Numéricas")
variable_pairs = [
    ("Temperatura", "Produção"),
    ("Precipitação", "Produção"),
    ("Umidade", "Produção"),
    ("Temperatura", "Precipitação"),
    ("Temperatura", "Umidade"),
]
for x_var, y_var in variable_pairs:
    fig = px.scatter(df, x=x_var, y=y_var, color="Fertilizante", symbol="Tipo de Solo", title=f"{x_var} vs {y_var}")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Distribuição de Produção por Fertilizante e Tipo de Solo")
fig = px.violin(df, x="Fertilizante", y="Produção", box=True, points="all", title="Distribuição de Produção por Fertilizante")
st.plotly_chart(fig, use_container_width=True)
fig = px.violin(df, x="Tipo de Solo", y="Produção", box=True, points="all", title="Distribuição de Produção por Tipo de Solo")
st.plotly_chart(fig, use_container_width=True)

st.header("5. Análise de Correlação")
st.subheader("Mapa de Calor de Correlação")
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()
fig_heatmap, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig_heatmap)

st.header("6. Análise Multivariada")
st.subheader("Pair Plot das Variáveis Numéricas")
df_encoded = df.copy()
df_encoded["Fertilizante"] = df_encoded["Fertilizante"].map({"Orgânico": 0, "Sintético": 1})
df_encoded["Tipo de Solo"] = df_encoded["Tipo de Solo"].map({"Arenoso": 0, "Argiloso": 1, "Siltoso": 2})
fig = sns.pairplot(df_encoded, hue="Fertilizante", vars=numeric_columns, diag_kind="kde", corner=True)
st.pyplot(fig)

st.header("7. Análise Interativa")
st.subheader("Gráfico de Dispersão Interativo")
col1, col2, col3 = st.columns(3)
with col1:
    x_var = st.selectbox("Selecione a Variável X", numeric_columns)
with col2:
    y_var = st.selectbox("Selecione a Variável Y", numeric_columns)
with col3:
    color_var = st.selectbox("Selecione a Variável de Cor", categorical_columns)
corr_temp_prod = df[x_var].corr(df[y_var])
st.write(f"Correlação de Pearson entre {y_var} e {x_var}: {corr_temp_prod:.2f}")
fig = px.scatter(df, x=x_var, y=y_var, color=color_var, title=f"{x_var} vs {y_var} por {color_var}")
st.plotly_chart(fig, use_container_width=True)
