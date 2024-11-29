import streamlit as st

inicio = st.Page("inicio.py", title="Início", icon="🏡", default=True)
analise_dados = st.Page("analise_de_dados.py", title="Análise de Dados", icon="📊")
modelagem_preditiva = st.Page("modelagem_preditiva.py", title="Modelagem Preditiva", icon="✨")
nav = st.navigation(
    {
        "Farmtech Análise Agrícola": [inicio, analise_dados, modelagem_preditiva],
    }
)
nav.run()
