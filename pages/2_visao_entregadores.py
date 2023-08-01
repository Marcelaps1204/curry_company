import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title= 'Visão Entregadores', page_icon =' ', layout='wide')


#================================================================
#-------------------FUNÇÕES--------------------------------------
#================================================================
def top_delivers_fast (df1):
    df1_06 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)']).reset_index()

                
    df_city1 = df1_06.loc[df1_06['City'] == 'Metropolitian', :].head(10)
    df_city2 = df1_06.loc[df1_06['City'] == 'Urban', :].head(10)
    df_city3 = df1_06.loc[df1_06['City'] == 'Semi-Urban', :].head(10)

    df1_07 = pd.concat([df_city1, df_city2, df_city3]).reset_index (drop=True)
    return df1_07


def top_delivers_slow (df1):
    df1_07 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending= False).reset_index()

    df_cityM = df1_07.loc[df1_07['City'] == 'Metropolitian', :].head(10)
    df_cityU = df1_07.loc[df1_07['City'] == 'Urban', :].head(10)
    df_cityS = df1_07.loc[df1_07['City'] == 'Semi-Urban', :].head(10)

    df1_08 = pd.concat([df_cityM, df_cityU, df_cityS]).reset_index (drop=True)
    return df1_08


def clean_code (df1):
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

#df1.head()

#================================
# Barra Lateral
#================================

st.header('Marketplace - Visão Entregadores')

image=Image.open('logo1.png')

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('##Selecione uma data limite')
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


#================================
# Layout Streamlit
#================================

tab1, tab2 = st.tabs (['Visão Gerencial', 'Gráficos'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns (4, gap='large')
        with col1:
            
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
            
        with col2:
            
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade) 
            
        with col3:                          
           
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor Condição de Veículo', melhor_condicao)
            
        with col4:
           
            pior_condicao = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior Condição de Veículo', pior_condicao)
            
    with st.container():
        st.markdown("""___""")
        st.title('Avaliações Médias')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Entregador')
            df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown('##### Densidade de Tráfego')
            df_avg_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']}))
            df_avg_traffic.columns = ['Delivery_mean', 'Delivery_std']
            df_avg_traffic = df_avg_traffic.reset_index()
            st.dataframe(df_avg_traffic)

            
            st.markdown('##### Condição Climática')
            df_avg_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']}))
            df_avg_weather.columns = ['mean', 'std']
            df_avg_weather = df_avg_weather.reset_index()
            st.dataframe(df_avg_weather)
            
            
    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns (2, gap='small')
        with col1:
            st.markdown('##### Top 10 Entregadores mais Rápidos')
            df1_07 = top_delivers_fast (df1)
            st.dataframe(df1_07)
            
        with col2:
            st.markdown('##### Top 10 Entregadores mais Lentos')
            df1_08 = top_delivers_slow (df1)
            st.dataframe (df1_08)
            
            
with tab2:
    with st.container():
        st.title('Gráficos')
        col1, col2 = st.columns (2, gap='large')
        with col1:
            st.markdown('##### Média de Idade dos Entregadores por Cidade')
            df1_media = df1[['Delivery_person_Age','City']].groupby('City').mean().reset_index()

            fig = px.pie (df1_media, values='Delivery_person_Age', names='City')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown('##### Média das avalições feitas por condições climáticas')
            media_clima = df1[['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').mean().reset_index()
            fig = px.pie(media_clima, values='Delivery_person_Ratings', names='Weatherconditions')
            st.plotly_chart(fig, use_container_width=True)
            
    with st.container():
        st.markdown('##### Total de Entregas Diárias, Feitas por Densidade de Tráfego Low e Jam')
        densidade = df1.loc[(df1['Road_traffic_density'] == 'Low') | (df1['Road_traffic_density'] == 'Jam')]

        densidade = densidade[['Order_Date', 'ID']].groupby('Order_Date').count().reset_index()

        densidade.columns = ['Order_Date', 'Numbers_of_deliveries']

        fig = px.line(densidade, x='Order_Date', y='Numbers_of_deliveries')
        
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        st.markdown ('##### Avaliações Médias das Entregas por Semana')
        df1['Week_of_year'] = df1['Order_Date'].dt.strftime ('%U')
        df1_avg2 = df1.loc[:,['Delivery_person_Ratings', 'Week_of_year']].groupby('Week_of_year').mean().reset_index()
        fig = px.bar(df1_avg2, x='Week_of_year', y='Delivery_person_Ratings', title='Média das Avaliações das Entregas por Semana', color='Week_of_year', text_auto=True)           
        st.plotly_chart(fig, use_container_width=True)
        