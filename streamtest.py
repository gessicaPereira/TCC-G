import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import textwrap


from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
##import cv2
import pandas as pd
#from st_aggrid import AgGrid
import plotly.express as px
import io 

df = pd.read_csv('estabcnaeok.csv')


#MENU QUE PRECISA DE AJUSTE
with st.sidebar:
    choose = option_menu("Menu", ["Sobre", "Estabelecimentos", "Localizações"],
                         icons=['house', 'shop', 'pin'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    }
    )

#logo = Image.open(r'C:\Users\08897\TCC\BASECOMPLETA\gatoum.jpg')
#profile = Image.open(r'C:\Users\08897\TCC\BASECOMPLETA\gatodois.jpg')
if choose == "Estabelecimentos": 
    st.text('Testando 1')

    #col1, col2 = st.columns( [0.8, 0.2])
    #with col1:               # To display the header text using css style
     #   st.markdown(""" <style> .font {
      #      font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
       #     </style> """, unsafe_allow_html=True)
        #st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)    
    #with col2:               # To display brand log
     #   st.image(logo, width=130 )
    
    #st.write("Please visit My Data Talk's Medium blog at: https://medium.com/@insightsbees")    
    #st.image(profile, width=700 )
elif choose == "Localizações":
    st.text('Testando 2')


#MENU

#
#with st.sidebar: 
 #   selected = option_menu("Menu", ["Home Settings", "Teste"],
  #                         icons=['house', 'gear'], menu_icon="cast", default_index=0)
    
   # if selected == "Teste":
    #    st.write("Página de teste")
    #else:
     #   st.write("Outra página")

  #  selected


#COMEÇA A APLICAÇÃO ---->

#df2 = pd.read_csv('estabelecimentos_total_dataok.csv')


    #INICIO GRÁFICO 1 - PRA MIM GRÁFICO 1 ESTÁ OK
df['DATA STC'] = pd.to_datetime(df['DATA STC'])

# AQUI EU VOU ACESSAR A PROPIEDADE ANO DA DATA DE SITUAÇÃO CADASTRAL PARA AGRUPAR E CONTAR A PARTIR DO 
# CNPJ O QUANTOS CNPJS CORRESPONDEM AQUELE ANO 
# A VARIAVEL ARMAZENA OS ANOS COMO INDICE E A CONTAGEM DOS ESTABELECIMENTOS COM OS VALORES CORRESPONDENTES
contagem_anos = df.groupby(df['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

# O GRÁFICO COM O EFEITO HOVER
fig = go.Figure(data=go.Scatter(x=contagem_anos['DATA STC'], y=contagem_anos['CNPJ O'],
                               mode='lines+markers', hovertext=df['CNPJ O'],
                               hovertemplate='CNPJ: %{hovertext}<br>Quantidade: %{y}<extra></extra>'))

# O LAYOUT DO GRÁFICO
fig.update_layout(
title='Número de estabelecimentos por ano',
xaxis_title='Ano',
yaxis_title='Quantidade de Estabelecimentos',
title_x=0.28,
title_font=dict(size=20)
)

st.plotly_chart(fig) 
#FIM GRÁFICO 1


#GRAFICO 2 - NÃO FICOU MUITO BOM
#contagem_atividades = df['CNAE PRINCP'].value_counts()

#top_3_atividades = contagem_atividades.nlargest(3)

#plt.rcParams['font.size'] = 12

#plt.figure(figsize=(10, 20))
#labels = [textwrap.fill(atividade, 15) for atividade in top_3_atividades.index]
#plt.pie(top_3_atividades.values, labels=top_3_atividades.index, autopct='%1.1f%%', startangle=140)
#plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#plt.title('As 3 Atividades Econômicas Mais Frequentes na Cidade Específica')
#plt.tight_layout()

#st.pyplot(plt)




#GRAFICO 3 - ESSE DAQUI PODE SER COLOCADO NO DA PIZZA E TER AS 10 ATIVIDADES LÁ
#contagem_atividades = df['CNAE PRINCP'].value_counts()

#top_10_atividades = contagem_atividades.nlargest(10)

#fig = px.bar(x=top_10_atividades.index, y=top_10_atividades.values,  labels={'x': 'Atividade Econômicaz', 'y': 'Quantidade'},
 #            title='Top 10 Atividades Econômicas Mais Comuns na Cidade Específica')

#fig.update_xaxes(tickmode='array', tickvals=[])

#fig.update_yaxes(title_text='Quantidade de estabelecimentos', title_font_size=10)


#fig = px.bar(x=top_10_atividades.index, y=top_10_atividades.values, labels={'x': 'Atividade Econômica', 'y': 'Quantidade'},
 #            title='Top 10 Atividades Econômicas Mais Comuns na Cidade Específica')


#fig.update_yaxes(title_text='Quantidade estabelecimentos', title_font_size=8)

#st.plotly_chart(fig)


#GRAFICO 4
#fig = px.histogram(df, x='DT IN ATV', nbins=20,
 #                  title='Distribuição dos Anos de Início da Atividade dos Estabelecimentos')

#fig.update_xaxes(title_text='Ano de Início')
#fig.update_yaxes(title_text='Quantidade')
#st.plotly_chart(fig)

#LEGAL ESSE, VERIFICAR DEPOIS SE ELE VAI FICAR 
#GRAFICO 5
fig = px.density_heatmap(df, x='DT IN ATV', title='Distribuição de Estabelecimentos')
fig.update_xaxes(title_text='Ano de Início')

fig.update_yaxes(title_text='Densidade')

fig.update_layout(
title_x=0.28,
title_font=dict(size=20))

st.plotly_chart(fig)


#with st.sidebar: 
 #   selected = option_menu("Menu", ["Home Settings", "Teste"],
  #                         icons=['house', 'gear'], menu_icon="cast", default_index=0)
    
#if selected == "Teste":
 #   st.write("Página de teste")
        
  #  fig = px.density_heatmap(df, x='DT IN ATV', title='Distribuição dos Anos de Início da Atividade - Densidade')
   # fig.update_xaxes(title_text='Ano de Início')

    #fig.update_yaxes(title_text='Densidade')

    #st.plotly_chart(fig)
#elif selected == "Home Settings":
 #   st.write("Outra página")


contagem_atividades = df['CNAE PRINCP'].value_counts()
top_3_atividades = contagem_atividades.nlargest(3)

# Cria um DataFrame com os dados das atividades econômicas mais frequentes
top_3_df = pd.DataFrame({'Atividade': top_3_atividades.index, 'Frequência': top_3_atividades.values})

# Cria um gráfico de pizza interativo usando o Plotly Express
fig = px.pie(top_3_df, values='Frequência', names='Atividade')

fig.update_layout(
    title='Três atividades econômicas mais presentes',
    height=450,
    title_font=dict(size=20),
    title_x=0.25,
    width=800, 
    legend=dict(
        orientation='h'
    )
)

st.plotly_chart(fig)

#from geopy.geocoders import Nominatim
#import folium

# Carrega o DataFrame com os dados do arquivo CSV
#df = pd.read_csv('seuarquivo.csv')

# Cria um objeto geocoder do Nominatim
#geolocator = Nominatim(user_agent="geoapiExercises")

# Função para obter as coordenadas de latitude e longitude
#def get_coordinates(address):
 #   location = geolocator.geocode(address)
  #  if location:
   #     return location.latitude, location.longitude
    #return None, None

# Adiciona colunas de latitude e longitude ao DataFrame
#df['latitude'], df['longitude'] = zip(*df.apply(lambda row: get_coordinates(f"{row['TIPO LOGR']}, {row['LOGRD']}, {row['BAIRRO']}, {row['MUNICIPIO']}, {row['UF']},"), axis=1))

# Filtra apenas os registros com coordenadas válidas
#df = df.dropna(subset=['latitude', 'longitude'])

# Cria um mapa inicial
#m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# Adiciona marcadores para cada estabelecimento no mapa
#for index, row in df.iterrows():
 #   folium.Marker(
  #      location=[row['latitude'], row['longitude']],
   #     popup=row['NOME FANT'],
    #    icon=folium.Icon(icon='cloud')  # Escolha o ícone que desejar
    #).add_to(m)



#st.markdown(m._repr_html_(), unsafe_allow_html=True)


st.title('Pesquisa de Estabelecimentos')

name_local = st.text_input('Digite o nome do estabelecimento:')

filter_local = df[df['NOME FANT'].str.contains(name_local, case=False)]

if not filter_local.empty:
    st.subheader('Informações do Estabelecimento')
    st.write('Nome:', filter_local['NOME FANT'].iloc[0])
    st.write('Data de Início da Atividade:', filter_local['DT IN ATV'].iloc[0])
    st.write('Localização:', filter_local['LOGRD'].iloc[0])
else:
    st.error('Nenhum estabelecimento encontrado com esse nome.')
















