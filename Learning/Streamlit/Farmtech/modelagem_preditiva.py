import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from data_generator import generate_data

@st.cache_resource
def load_model():
    _model = RandomForestRegressor()
    return _model

st.set_page_config(
    page_title="Modelagem Preditiva",
    layout="wide"
)
st.title("Modelagem Preditiva")

st.header("1. Carregar e Filtrar os Dados")
df = generate_data()

st.sidebar.title("Filtros de Dados")
selected_fertilizer = st.sidebar.multiselect(
    "Selecione os Fertilizantes",
    df["Fertilizante"].unique(),
    default=df["Fertilizante"].unique()
)
selected_soil = st.sidebar.multiselect(
    "Selecione os Tipos de Solo",
    df["Tipo de Solo"].unique(),
    default=df["Tipo de Solo"].unique()
)
st.sidebar.subheader("Intervalos das Variáveis Numéricas")
temp_min, temp_max = st.sidebar.slider(
    "Temperatura (°C)",
    min_value=df["Temperatura"].min(),
    max_value=df["Temperatura"].max(),
    value=(df["Temperatura"].min(), df["Temperatura"].max())
)
precip_min, precip_max = st.sidebar.slider(
    "Precipitação (mm)",
    min_value=df["Precipitação"].min(),
    max_value=df["Precipitação"].max(),
    value=(df["Precipitação"].min(), df["Precipitação"].max())
)
humidity_min, humidity_max = st.sidebar.slider(
    "Umidade (%)",
    min_value=df["Umidade"].min(),
    max_value=df["Umidade"].max(),
    value=(df["Umidade"].min(), df["Umidade"].max())
)

filtered_df = df[
    (df["Fertilizante"].isin(selected_fertilizer)) &
    (df["Tipo de Solo"].isin(selected_soil)) &
    (df["Temperatura"] >= temp_min) & (df["Temperatura"] <= temp_max) &
    (df["Precipitação"] >= precip_min) & (df["Precipitação"] <= precip_max) &
    (df["Umidade"] >= humidity_min) & (df["Umidade"] <= humidity_max)
]
if filtered_df.empty:
    st.write("Nenhum dado encontrado. Por favor, ajuste os filtros.")
else:
    st.subheader("Dados Filtrados")
    st.dataframe(filtered_df.head(), use_container_width=True, hide_index=True)

st.header("2. Preparar os Dados para Modelagem")
ml_df = pd.get_dummies(filtered_df, columns=["Fertilizante", "Tipo de Solo"])
x = ml_df.drop('Produção', axis=1)
y = ml_df['Produção']

if len(x) < 2:
    st.warning("Dados insuficientes para treinamento. Por favor, ajuste os filtros.")
    st.stop()
else:
    st.write(f"**Quantidade de dados para treinamento:**", len(x))

st.header("3. Treinamento do Modelo de Machine Learning")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = load_model()
model.fit(x_train, y_train)
score = model.score(x_test, y_test)
st.write(f"**Acurácia do modelo (R² no conjunto de teste):**", round(score, 2))

st.header("4. Fazer Previsões de Produção com o Modelo")
st.subheader("Insira os Dados para Previsão")
input_temp = st.slider("Temperatura (°C)", min_value=-20, max_value=50, value=22)
input_precip = st.slider("Precipitação (mm)", min_value=0, max_value=500, value=100)
input_humidity = st.slider("Umidade (%)", min_value=0, max_value=100, value=50)
input_fertilizer = st.selectbox("Fertilizante", df["Fertilizante"].unique())
input_soil = st.selectbox("Tipo de Solo", df["Tipo de Solo"].unique())
input_data = {
    "Temperatura": [input_temp],
    "Precipitação": [input_precip],
    "Umidade": [input_humidity],
    "Fertilizante_Orgânico": [1 if input_fertilizer == "Orgânico" else 0],
    "Fertilizante_Sintético": [1 if input_fertilizer == "Sintético" else 0],
    "Tipo de Solo_Arenoso": [1 if input_soil == "Arenoso" else 0],
    "Tipo de Solo_Argiloso": [1 if input_soil == "Argiloso" else 0],
    "Tipo de Solo_Siltoso": [1 if input_soil == "Siltoso" else 0]
}
input_df = pd.DataFrame(input_data)
for col in x.columns:
    if col not in input_df.columns:
        input_df[col] = 0
input_df = input_df[x.columns]
prediction = model.predict(input_df)
st.subheader("Resultado da Previsão")
st.write(f"**Previsão de Produção:**", round(prediction[0], 2), "ton/ha")
