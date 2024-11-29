import streamlit as st

st.set_page_config(
    page_title="Farmtech Análise Agrícola",
    page_icon=":tractor:",
    layout="wide"
)

st.title("Farmtech Análise Agrícola :tractor:")
st.write("Análise da produção agrícola em diferentes regiões do Brasil.")

st.markdown(
    """
    Este aplicativo permite explorar um dataset simulado de produção agrícola,
    realizar análises exploratórias e aplicar modelos preditivos.
    Utilize o menu lateral para navegar pelo aplicativo.
    """
)
