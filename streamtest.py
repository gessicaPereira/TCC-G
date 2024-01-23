import streamlit as st
import pandas as pd 
from plotly import graph_objs as go

from streamlit_option_menu import option_menu
##import cv2
import pandas as pd
#from st_aggrid import AgGrid
import plotly.express as px



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

    col1, col2 = st.columns([0.4, 2])
    
#INICIO GRÁFICO 1 - PRA MIM GRÁFICO 1 ESTÁ OK - OK COM O FILTRO
    df['DATA STC'] = pd.to_datetime(df['DATA STC'])

# AQUI EU VOU ACESSAR A PROPIEDADE ANO DA DATA DE SITUAÇÃO CADASTRAL PARA AGRUPAR E CONTAR A PARTIR DO 
# CNPJ O QUANTOS CNPJS CORRESPONDEM AQUELE ANO 
# A VARIAVEL ARMAZENA OS ANOS COMO INDICE E A CONTAGEM DOS ESTABELECIMENTOS COM OS VALORES CORRESPONDENTES
    contagem_anos = df.groupby(df['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

    with col1: 
        selected_years = st.slider("Selecione o intervalo de anos", int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max()), (int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max())))
        filtered_data = contagem_anos[(contagem_anos['DATA STC'] >= selected_years[0]) & (contagem_anos['DATA STC'] <= selected_years[1])]

    with col2:
#efeito hover
        fig = go.Figure(data=go.Scatter(x=filtered_data['DATA STC'], y=filtered_data['CNPJ O'],
                                mode='lines+markers', hovertext=df['CNPJ O'],
                                hovertemplate='CNPJ: %{hovertext}<br>Quantidade: %{y}<extra></extra>'))

        fig.update_layout(
        title='Números Anuais de Novos Estabelecimentos na Cidade',
        xaxis_title='Ano',
        yaxis_title='Quantidade de Estabelecimentos',
        title_x=0.21,
        title_font=dict(size=20),
        width= 750
        )
        st.plotly_chart(fig) 
    #fim grafico 1


#INICIO GRÁFICO INATIVAS - OK - NÃO MEXER MAIS
    df_inativas['DATA STC'] = pd.to_datetime(df_inativas['DATA STC'])

    contagem_anos = df_inativas.groupby(df_inativas['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

    col1, col2 = st.columns([0.4, 2])

    with col1:
        selected_years = st.slider("Selecione o intervalo de anos", int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max()), (int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max())))
        filtered_data = contagem_anos[(contagem_anos['DATA STC'] >= selected_years[0]) & (contagem_anos['DATA STC'] <= selected_years[1])]

    with col2:
        fig = px.bar(filtered_data, x='DATA STC', y='CNPJ O', title='Números Anuais de Estabelecimentos Inativos na Cidade')

        fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Quantidade ',
        title_x=0.21,
        title_font=dict(size=20),
        width=750,
        barmode='stack')
    
        st.plotly_chart(fig)

#fim grafico 1

 #INICIO GRAFICO 2 - OK COM O FILTRO 
    col1, col2 = st.columns([0.4, 2])
    contagem_atividades = df['CNAE PRINCP'].value_counts()

    with col1: 
        num_atividades_para_mostrar = st.slider("Selecione o número de atividades a serem exibidas", 1, len(contagem_atividades), 3)
        top_atividades = contagem_atividades.nlargest(num_atividades_para_mostrar)

    with col2: 

        top_df = pd.DataFrame({'Atividade': top_atividades.index, 'Frequência': top_atividades.values})

        fig = px.pie(top_df, values='Frequência', names='Atividade')

        fig.update_layout(
        title=f'Cenário Empresarial: As {num_atividades_para_mostrar} Atividades que Dominam a Economia Local',
        height=450,
        title_font=dict(size=20),
        title_x=0.08,
        width=800, 
        legend=dict(
            orientation='h'))
        st.plotly_chart(fig)

#INICIO GRAFICO 3 - inativos - OK COM O FILTRO
    col1, col2 = st.columns([0.4, 2])
    contagem_atividades_inativas = df_inativas['CNAE PRINCP'].value_counts()

    with col1: 
        num_atividades_inativas_para_mostrar = st.slider("Selecione o número de atividades a serem exibidas", 1, len(contagem_atividades_inativas), 3)
        top_atividades_inativas = contagem_atividades_inativas.nlargest(num_atividades_inativas_para_mostrar)

    with col2:
        top_df_inativas = pd.DataFrame({'Atividade': top_atividades_inativas.index, 'Frequência': top_atividades_inativas.values})

        fig = px.bar(top_df_inativas, y='Atividade', x='Frequência', labels={'Frequência': 'Contagem'})

        fig.update_traces(hovertemplate='%{y}: %{x}')
        fig.update_layout(
            title=f'Tendências de encerramento: As {num_atividades_inativas_para_mostrar} Atividades Econômicas mais Afetadas na Cidade',
            height=450,
            title_x=0.06,
            title_font=dict(size=20),
            width=800,
            legend=dict(orientation='h', font=dict(size=12))
        )
        st.plotly_chart(fig)

    
#filtro estabelecimentos ativos pela atividade selecionada
    st.markdown("""
    <style>
    .font {
    font-size: 30px !important;
    margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font">Encontrando Estabelecimentos por Classificação de Atividades Econômicas (CNAE) 🏢 </h5>', unsafe_allow_html=True)

    
    selected_activity = st.selectbox("Selecione a atividade:", df['CNAE PRINCP'].unique())

    filtered_estabelecimentos = df[df['CNAE PRINCP'] == selected_activity]

    #st.subheader(f" {selected_activity}")
    
    table_data = filtered_estabelecimentos[['NOME FANT', 'BAIRRO']]
    table_data.columns = ['Nome do Estabelecimento', 'Bairro']
    table_data = table_data.reset_index(drop=True)
    custom_css = """
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th {
                border-bottom: 2px solid #dddddd;
                color: #555555;
                background-color: #f9f9f9;
            }
            th, td {
                text-align: left;
                border: none!important;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.table(table_data)

    st.markdown("""
    <style>
    .font2 {
    font-size: 30px !important;
    margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font2">Distribuição por Bairro 📊 </h5>', unsafe_allow_html=True)

    total_estabelecimentos = len(filtered_estabelecimentos)
    bairro_counts = filtered_estabelecimentos['BAIRRO'].value_counts()
    bairro_counts_df = pd.DataFrame({'Bairro': bairro_counts.index, 'Contagem': bairro_counts.values})
    st.write(f" 🔵 Total de Estabelecimentos: {total_estabelecimentos}")
    st.bar_chart(bairro_counts_df.set_index('Bairro'))



elif choose == "Localizações":

    #PESQUISA ESTABELECIMENTOS  
    st.markdown("""
    <style>
    .font {
    font-size: 39px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font">Busca por estabelecimento  </h5>', unsafe_allow_html=True)
    #st.write("Digite o nome do estabelecimento no campo abaixo para obter informações")
    name_local = st.text_input(label='Digite o nome do estabelecimento: ', placeholder='Pesquisar                                                                                                                                                                                          🔍')
    filter_local = df[df['NOME FANT'].str.contains(name_local, case=False)]

    if not filter_local.empty:
        #st.subheader('Informações do estabelecimento')
        st.markdown(
        """
        <div style='background-color: #F8F9FA; padding: 10px; border-radius: 10px;'>
            <h5>Informações do estabelecimento 📌 </h5>
            <p><strong> {}</p></strong>
            <p><strong>DATA DE INÍCIO DA ATIVIDADE:</strong> {}</p>
            <p><strong>LOCALIZAÇÃO:</strong> {}</p>
        </div>
        """.format(filter_local['NOME FANT'].iloc[0], filter_local['DT IN ATV'].iloc[0], filter_local['LOGRD'].iloc[0]),
        unsafe_allow_html=True
    )
    else:
        st.error('Nenhum estabelecimento encontrado com esse nome.')

#MAPA
    import folium
    from streamlit_folium import st_folium

    dfloc = pd.read_csv('estabGeolocalizadoOK.csv')

    st.markdown("""
    <style>
    .font {
    font-size: 30px !important;
    margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font">Distribuição dos estabelecimentos na cidade 🗺️ </h5>', unsafe_allow_html=True)

    m = folium.Map(location=[dfloc['Latitude'].mean(), dfloc['Longitude'].mean()], zoom_start=9)

    for index, row in dfloc.iterrows():
        folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['NOME FANT'],  
        icon=folium.Icon(icon='home')  
    ).add_to(m)

    st_data = st_folium(m, width=900, height=400)
    #st.write(st_data)

elif choose == "Sobre":
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("""
        <style>
        .fontS {
        font-size: 40px !important;
        margin-top: 140px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<h1 class="fontS"> Cedro Localize </h1>', unsafe_allow_html=True)

        st.markdown('Aplicação desenvolvida como trabalho de conclusão do curso bacharelado em Sistemas de Informação do IFCE campus Cedro.')
        #st.markdown('Esaa interface foi desenvolvida com o intuito de auxiliar no processo decisório de novos empreendedores da cidade de Cedro no Ceará, bem como disponibilizar uma visão mais ampla acerca do empreendedorismo local.')

    with col2:    
        url_img = "1111.jpg"
        st.image(url_img, width=520)





#teste pro grafico das localizações
#import folium
import folium
from streamlit_folium import st_folium

# center on Liberty Bell, add marker
#m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
#folium.Marker(
#    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
#).add_to(m)

# call to render Folium map in Streamlit
#st_data = st_folium(m, width=725)
