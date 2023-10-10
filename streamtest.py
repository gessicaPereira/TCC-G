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


##AJUSTAR ISSO É O TITULO DA PÁGINA 
#st.set_page_config(
  #  page_title="Pesquisa de Estabelecimentos",
   # page_icon="🏢",
    #layout="wide",
#)


df = pd.read_csv('estabcnaeok.csv')
df_inativas = pd.read_csv('estab_inativos_ok.csv')


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

    col1, col2 = st.columns(2)
    
        #INICIO GRÁFICO 1 - PRA MIM GRÁFICO 1 ESTÁ OK
    df['DATA STC'] = pd.to_datetime(df['DATA STC'])

# AQUI EU VOU ACESSAR A PROPIEDADE ANO DA DATA DE SITUAÇÃO CADASTRAL PARA AGRUPAR E CONTAR A PARTIR DO 
# CNPJ O QUANTOS CNPJS CORRESPONDEM AQUELE ANO 
# A VARIAVEL ARMAZENA OS ANOS COMO INDICE E A CONTAGEM DOS ESTABELECIMENTOS COM OS VALORES CORRESPONDENTES
    contagem_anos = df.groupby(df['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

#efeito hover
    fig = go.Figure(data=go.Scatter(x=contagem_anos['DATA STC'], y=contagem_anos['CNPJ O'],
                               mode='lines+markers', hovertext=df['CNPJ O'],
                               hovertemplate='CNPJ: %{hovertext}<br>Quantidade: %{y}<extra></extra>'))

    fig.update_layout(
    title='Número de estabelecimentos por ano',
    xaxis_title='Ano',
    yaxis_title='Quantidade de Estabelecimentos',
    title_x=0.28,
    title_font=dict(size=20),
    width= 750
    )
    st.plotly_chart(fig) 
    #fim grafico 1


    #INICIO GRÁFICO INATIVAS 
    df_inativas['DATA STC'] = pd.to_datetime(df_inativas['DATA STC'])

    contagem_anos = df_inativas.groupby(df_inativas['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

    selected_years = st.slider("Selecione o intervalo de anos", int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max()), (int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max())))
    fig = px.bar(contagem_anos, x='DATA STC', y='CNPJ O', title='Número de estabelecimentos inativos')

    fig.update_layout(
    xaxis_title='Ano',
    yaxis_title='Quantidade ',
    title_x=0.30,
    title_font=dict(size=20),
    width=750,
    barmode='stack'  
    )

#filtro dos dados baseado no intervalo de anos selecionado
    filtered_data = contagem_anos[(contagem_anos['DATA STC'] >= selected_years[0]) & (contagem_anos['DATA STC'] <= selected_years[1])]

    fig.data[0].x = filtered_data['DATA STC']
    fig.data[0].y = filtered_data['CNPJ O']


    st.plotly_chart(fig) 
    #fim grafico 1

    #INICIO GRAFICO 2
    contagem_atividades = df['CNAE PRINCP'].value_counts()
    top_3_atividades = contagem_atividades.nlargest(3)

    top_3_df = pd.DataFrame({'Atividade': top_3_atividades.index, 'Frequência': top_3_atividades.values})

    fig = px.pie(top_3_df, values='Frequência', names='Atividade')

    fig.update_layout(
    title='Três atividades econômicas mais presentes',
    height=450,
    title_font=dict(size=20),
    title_x=0.25,
    width=800, 
    legend=dict(
        orientation='h'))
    st.plotly_chart(fig)

    #INICIO GRAFICO 3 - inativos
    contagem_atividades_inativas = df_inativas['CNAE PRINCP'].value_counts()
    top_3_atividades_inativas = contagem_atividades_inativas.nlargest(3)

    top_3_df_inativas = pd.DataFrame({'Atividade': top_3_atividades_inativas.index, 'Frequência': top_3_atividades_inativas.values})

    fig = px.pie(top_3_df_inativas, values='Frequência', names='Atividade')

    fig.update_layout(
    title='Atividades econômicas inativas',
    height=450,
    title_font=dict(size=20),
    title_x=0.25,
    width=800, 
    legend=dict(
        orientation='h'))
    st.plotly_chart(fig)

elif choose == "Localizações":
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
elif choose == "Sobre":
    st.title('Aplicação TCC - nome')
    st.markdown('Aplicação desenvolvida como trabalho de conclusão do curso bacharelado em Sistemas de Informação.')
    st.markdown('Esaa interface foi desenvolvida com o intuito de auxiliar no processo decisório de novos empreendedores da cidade de Cedro no Ceará, bem como disponibilizar uma visão mais ampla acerca do empreendedorismo local.')




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






#teste pro grafico das localizações
#import folium
#import streamlit as st

#from streamlit_folium import st_folium

# center on Liberty Bell, add marker
#m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
#folium.Marker(
 #   [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
#).add_to(m)

# call to render Folium map in Streamlit
#st_data = st_folium(m, width=725)



# Página principal do Streamlit
def main():
    st.title("CNAES")

    # Filtro por atividade
    selected_activity = st.selectbox("Filtrar por atividade", df['CNAE PRINCP'].unique())

    # Filtrar estabelecimentos ativos pela atividade selecionada
    filtered_estabelecimentos = df[df['CNAE PRINCP'] == selected_activity]

    st.subheader(f" {selected_activity}")
    
    table_data = filtered_estabelecimentos[['NOME FANT', 'BAIRRO']]
    st.table(table_data)
if __name__ == "__main__":
    main()


import folium

dfloc = pd.read_csv('estabGeolocalizado.csv')

m = folium.Map(location=[dfloc['Latitude'].mean(), dfloc['Longitude'].mean()], zoom_start=12)

for index, row in dfloc.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['LOGRD'],  
        icon=folium.Icon(icon='cloud')  
    ).add_to(m)

st.title('Mapa de Localizações')
st.write('Visualização de localizações a partir das coordenadas de latitude e longitude.')
st.write(m)























