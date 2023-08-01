import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title= 'Visão Empresa', page_icon =' ', layout='wide')

#================================================================
#-------------------FUNÇÕES--------------------------------------
#================================================================

def country_maps(df1):
    colunas = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    colunas_agrupadas = ['City', 'Road_traffic_density']

    data_map = df1.loc[:, colunas].groupby( colunas_agrupadas ).median().reset_index()
    data_map = data_map[data_map['City'] != 'NaN']
    data_map = data_map[data_map['Road_traffic_density'] != 'NaN']

    map_ = folium.Map( zoom_start=11 )
    
    for index, location_info in data_map.iterrows():
            folium.Marker( [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )
            
    folium_static(map_ , width=1024, height=600)

def order_share_by_week (df1):
    df1_aux5 = df1.loc[:, ['ID', 'Week_of_year']].groupby( 'Week_of_year' ).count().reset_index()

    df1_aux6 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby( 'Week_of_year').nunique().reset_index()

    df1_aux0 = pd.merge( df1_aux5, df1_aux6, how='inner' )

    df1_aux0['order_by_delivery'] = df1_aux0['ID'] / df1_aux0['Delivery_person_ID']

    fig = px.line(df1_aux0, x='Week_of_year', y='order_by_delivery')
        
    return fig

def order_by_week (df1):
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime ('%U')

    df1_aux2 = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    df1_aux2.columns = ['Entregas', 'Semana_do_Ano']

    fig = px.line(df1_aux2, x= 'Entregas', y='Semana_do_Ano', title= 'Quantidade de Pedidos por Semana')
    return fig

def traffic_order_city (df1):
    df1_aux4 = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()

    df1_aux4['Perc_ID'] = 100 * (df1_aux4['ID']/df1_aux4['ID'].sum())

    fig = px.scatter(df1_aux4, x= 'City', y='Road_traffic_density', size='ID', color='City')
    return fig

def traffic_order_share (df1):
    df1_aux3 = df1.loc[:, ['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

    df1_aux3['perc_ID'] = 100 * ( df1_aux3['ID'] / df1_aux3['ID'].sum() )
    fig = px.pie (df1_aux3,  values='perc_ID', names='Road_traffic_density' )
    return fig

def order_metric(df1):
    df1_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()

    df1_aux.columns = ['Order_Date', 'Entregas']

    fig = px.bar(df1_aux, x= 'Order_Date', y='Entregas')
    return fig

def clean_code( df1 ):
    """Esta funcao tem como responsabilidade limpar o dataframe
    Tipos de limpeza
        Remocao dos dados Nan
        Mudanca do tipo da coluna de dados
        Remocao dos espacos das variaveis de texto
        Formatacao da data
        Limpeza da coluna de tempo (remocao do texto da variavel numerica)
        
        Input Dataframe
        Output Dataframe"""
    
# Excluir as linhas com a idade dos entregadores vazia
# ( Conceitos de seleção condicional )
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

# Conversao de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

# Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

# Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime (df1['Order_Date'], format = '%d-%m-%Y')

# Remove as linhas da culuna multiple_deliveries que tenham o
# conteudo igual a 'NaN '
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)


# Removendo espaços dentro das strings sem usar o for, usando .str.strip()

    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply (lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


df= pd.read_csv('train.csv')

df1 = clean_code (df)


#================================
# Barra Lateral
#================================


st.header('Marketplace - Visão Empresa')

image=Image.open('logo1.png')

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?', 
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY')

#st.header(date_slider)
st.sidebar.markdown("""___""")


traffic_options=st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low','Medium', 'High', 'Jam',],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""___""")

weather_options=st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Sunny','conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy', 'conditions Fog', 'conditions Windy'],
    default=['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy', 'conditions Fog', 'conditions Windy'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

# filtro condições climáticas
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas,:]

#st.dataframe(df1)


#================================
# Layout Streamlit
#================================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    # Order Metric
    with st.container():
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share (df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)
              
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city (df1)
            st.plotly_chart(fig, use_container_width=True)                             
        
        
with tab2:
    with st.container():
        st.header('Orders by Week')
        fig = order_by_week (df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.header('Order Share by Week')
        fig = order_share_by_week (df1)
        st.plotly_chart(fig, use_container_width=True)
        
            
with tab3:
    
    st.header('Country Maps')
    country_maps(df1)
    
    
    


#print('Estou aqui')

