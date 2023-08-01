import streamlit as st
from PIL import Image

st.set_page_config (
    page_title= 'Home',
    page_icon=' ')

#image_path='Documents/REPOS/FTC_python_CDS/Dataset/delivery-man-g35bcb24a6_1280.png'
image=Image.open('logo1.png')
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.write('# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        -Visão Gerencial: Métricas Gerais de Comportamento.
        -Visão Tática: Indicadores Semanais de Crescimento.
        -Visão Geográfica: Insights de Geolocalização
    - Visão Entregadores:
        -Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        -Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Time de Data Science no Discord
        @meigarom
    """)
