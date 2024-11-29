import streamlit as st

inicio = st.Page("pages/0_inicio.py", title="Início", icon="🏡", default=True)
analise_dados = st.Page("pages/1_analise_de_dados.py", title="Análise de Dados", icon="📊")
modelagem_preditiva = st.Page("pages/2_modelagem_preditiva.py", title="Modelagem Preditiva", icon="✨")
nav = st.navigation(
    {
        "Farmtech Análise Agrícola": [inicio, analise_dados, modelagem_preditiva],
    }
)
nav.run()
