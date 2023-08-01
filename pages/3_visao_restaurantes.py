import plotly.express as px
import pandas as pd
from haversine import haversine
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
import numpy as np

st.set_page_config(page_title= 'Visão Restaurantes', page_icon =' ', layout='wide')


#================================================================
#-------------------FUNÇÕES--------------------------------------
#================================================================

def avg_std_time_on_traffic (df1):
    df1_aux05 = df1.loc[:,['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']})

    df1_aux05.columns = ['avg_city_traffic', 'std_city_traffic']

    df1_aux05 = df1_aux05.reset_index()
            
    fig = px.sunburst(df1_aux05, path=['City', 'Road_traffic_density'], values='avg_city_traffic', color='std_city_traffic', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df1_aux05['std_city_traffic']) )
    return fig


def avg_std_time_graph (df1):
    df1_aux = df1.loc[:,['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean', 'std']})

    df1_aux.columns = ['Avg_time', 'Std_time']

    df1_aux = df1_aux.reset_index()
            
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df1_aux['City'], y=df1_aux['Avg_time'], error_y=dict(type='data', array=df1_aux['Std_time']) ))
    fig.update_layout(barmode='group')        
    return fig


def avg_std_time_delivery(df1, festival, op):            
    df1_auxs = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)' : ['mean', 'std']})

    df1_auxs.columns = ['avg_time', 'std_time']

    df1_auxs = df1_auxs.reset_index()
    df1_auxs = np.round(df1_auxs.loc[df1_auxs['Festival']== festival, op],2)
    return df1_auxs
            
    
def distance (df1, fig):
    if fig == False:
        cols1 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

        df1['Distance'] = df1.loc[:, cols1].apply (lambda x: haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

        df1['Distance'] = df1['Distance'].astype(int)

        avg_distance = np.round(df1['Distance'].mean(),2)
        return avg_distance
    
    else:
        cols1 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

        df1['Distance'] = df1.loc[:, cols1].apply (lambda x: haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

        df1['Distance'] = df1['Distance'].astype(int)

        avg_distance = df1.loc[:,['City','Distance']].groupby('City').mean().reset_index()

        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['Distance'], pull=[0, 0.1,0])])
        return fig


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

#==================================
#--------Import Dataset------------
#==================================

df= pd.read_csv('train.csv')

#--------------------------------
#    Cleaning Code
#--------------------------------

df1 = clean_code (df)
#df1 = df.copy()
#df1.head()


#================================
# Barra Lateral
#================================

st.header('Marketplace - Visão Restaurantes')

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


tab1, tab2 = st.tabs(['Visão Gerencial', 'Gráficos'])
with tab1:
    with st.container():
        st.title('Overwall Metrics')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            unicos = df1.loc[:, 'Delivery_person_ID'].nunique()
            col1.metric('Entregadores Únicos', unicos) 
            
        with col2:
            avg_distance = distance (df1, fig=False)
            col2.metric('Distância Média', avg_distance)
                  
        with col3:
            df1_auxs = avg_std_time_delivery (df1, 'Yes', 'avg_time')
            col3.metric('Tempo Médio de Entrega no Festival', df1_auxs)
            
    with st.container():
        col1, col2, col3 = st.columns(3)
            
        with col1:
            df1_auxs = avg_std_time_delivery (df1, 'Yes', 'std_time')
            col1.metric('Desvio Padrão', df1_auxs)
            
        with col2:
            df1_auxs = avg_std_time_delivery (df1, 'No', 'avg_time')
            col2.metric('Tempo Médio de Entrega Sem Festival', df1_auxs)
            
        with col3: 
            df1_auxs = avg_std_time_delivery (df1, 'No', 'std_time')
            col3.metric('Desvio Padrão', df1_auxs)
            
    with st.container():
        st.markdown("""___""")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = avg_std_time_graph (df1)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:

            df1_aux04 = df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)' : ['mean', 'std']})

            df1_aux04.columns = ['Avg_city_order', 'Std_city_order']

            df1_aux04 = df1_aux04.reset_index()
            st.dataframe(df1_aux04, use_container_width=True)
        
        
    with st.container():
        st.markdown("""___""")
        st.title('Distribuição de Tempo')
        col1, col2 = st.columns ( [0.45, 0.55], gap='large')
        
        with col1:
            fig = distance (df1, fig=True)
            st.plotly_chart(fig, use_container_width=True)
            
            #df_aux = df1.loc[:,['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)' : ['mean' , 'std'] })
            #df_aux.columns = ['avg_time', 'std_time']
            #df_aux = df_aux.reset_index()
            
            #fig = go.Figure()
            #fig.add_trace ( go.Bar ( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
            #fig.update_layout(barmode='group')
            #st.plotly_chart(fig)
     
        with col2:    
            fig = avg_std_time_on_traffic (df1)
            st.plotly_chart(fig, use_container_width=True)
            
            
            
   # with st.container():
    #    st.markdown('###### Distância Média dos Restaurantes e dos Locais de Entrega')
     #   cols1 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

      #  df1['Distance'] = df1.loc[:, cols1].apply (lambda x: haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

       # df1['Distance'] = df1['Distance'].astype(int)

#        avg_distance = df1.loc[:,['City','Distance']].groupby('City').mean().reset_index()

 #       fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['Distance'], pull=[0, 0.1,0])])

  #      st.plotly_chart(fig, use_container_width=True)
        
   
        
            
            
            

            
        #with col2:
           # st.markdown('###### Tempo Médio de Entrega e Desvio Padrão por Cidade ')
            #cols3 = ['Time_taken(min)', 'City']
            #df1_aux03 = df1.loc[:,cols3].groupby('City').agg({'Time_taken(min)':['mean', 'std']})

            #df1_aux03.columns = ['Avg_time', 'Std_time']

            #df1_aux03.reset_index()
           
            #st.dataframe(df1_aux03) 
       # with col3:
       #     st.markdown('###### tempo médio e o desvio padrão de entrega por cidade e tipo de pedido')
      #     cols4 = ['Time_taken(min)', 'City', 'Type_of_order']
         #   df1_aux04 = df1.loc[:, cols4].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)' : ['mean', 'std']})

           # df1_aux04.columns = ['Avg_city_order', 'Std_city_order']

           # df1_aux04.reset_index()
           # st.dataframe(df1_aux04)
            
 
        