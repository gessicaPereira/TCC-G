import streamlit as st
import pandas as pd 
from plotly import graph_objs as go

from streamlit_option_menu import option_menu
##import cv2
import pandas as pd
#from st_aggrid import AgGrid
import plotly.express as px



##AJUSTAR ISSO É O TITULO DA PÁGINA 
st.set_page_config(
    page_title="Cedro Localize",
    page_icon="🏢",
    layout="wide",
)


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

    #INICIO DA AMOSTRAGEM DE ESTABELECIMENTOS ATIVOS ATUALMENTE  
    # Contar a quantidade total de estabelecimentos
    quantidade_estabelecimentos = df.shape[0]

    # HTML e CSS para criar o círculo com número dentro
    st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: transparent;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    ">
        <div style="text-align: center;">
            <p style="margin: 0; font-size: 48px; font-weight: bold; color: #FF4500;">{quantidade_estabelecimentos}</p>
            <h3 style="margin: 0; font-size: 24px; color: #FF4500;">Estabelecimentos Ativos em 2025</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
    )



    col1, col2 = st.columns([0.4, 2])
    
    # INICIO GRÁFICO 1 - COM FILTRO E GRÁFICO AJUSTADO
    df['DATA STC'] = pd.to_datetime(df['DATA STC'])

    # AQUI EU VOU ACESSAR A PROPIEDADE ANO DA DATA DE SITUAÇÃO CADASTRAL PARA AGRUPAR E CONTAR A PARTIR DO 
    # CNPJ O QUANTOS CNPJS CORRESPONDEM AQUELE ANO 
    # A VARIAVEL ARMAZENA OS ANOS COMO INDICE E A CONTAGEM DOS ESTABELECIMENTOS COM OS VALORES CORRESPONDENTES

    # Filtragem por intervalo de anos
    contagem_anos = df.groupby(df['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

    # Estilo centralizador (caso use para outros elementos)
    st.markdown("""
    <style>
        .center-container-g2 {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
    </style>
    """, unsafe_allow_html=True)

    # Usar colunas para centralizar slider e gráfico
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # Controle do filtro de intervalo de anos
        selected_years = st.slider(
            "Selecione o intervalo de anos",
            int(contagem_anos['DATA STC'].min()),
            int(contagem_anos['DATA STC'].max()),
            (int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max()))
        )

        # Filtrando os dados
        filtered_data = contagem_anos[(contagem_anos['DATA STC'] >= selected_years[0]) & (contagem_anos['DATA STC'] <= selected_years[1])]

        # Criação do gráfico de barras verticais
        fig = px.bar(filtered_data,
                    x='DATA STC',
                    y='CNPJ O',
                    labels={'CNPJ O': 'Quantidade de Estabelecimentos', 'DATA STC': 'Ano'},
                    title='Quantidade de Estabelecimentos Ativos por Ano',
                    text='CNPJ O',  # Exibe a quantidade no topo da barra
                    color='DATA STC',  # Cor das barras de acordo com o ano
                    color_continuous_scale='Viridis',  # Usando uma escala de cores profissional
                    template='plotly_dark',  # Usando template escuro para um visual mais moderno
                    orientation='v')  # Altera para barras verticais

        # Ajustar a posição do texto e o layout
        fig.update_traces(texttemplate='%{text}', textposition='outside', marker=dict(line=dict(width=0)))  # Coloca o texto fora da barra
        fig.update_layout(
            height=450,
            width=750,  # Ajuste o tamanho para combinar com o gráfico anterior
            title_x=0.2,
            title_font=dict(size=20),
            showlegend=False,  # Desabilita a legenda para um visual mais clean
            xaxis_title='Ano',
            yaxis_title='Quantidade de Estabelecimentos'
        )

        # Exibir o gráfico
        st.plotly_chart(fig)
    # FIM GRÁFICO 1


# INICIO GRÁFICO INATIVAS - OK - NÃO MEXER MAIS
    df_inativas['DATA STC'] = pd.to_datetime(df_inativas['DATA STC'])
    contagem_anos = df_inativas.groupby(df_inativas['DATA STC'].dt.year)['CNPJ O'].count().reset_index()

    # Estilo centralizador (caso use para outros elementos)
    st.markdown("""
    <style>
        .center-container-g2 {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
    </style>
    """, unsafe_allow_html=True)

    # Usar colunas para centralizar slider e gráfico
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        selected_years = st.slider(
            "Selecione o intervalo de anos",
            int(contagem_anos['DATA STC'].min()),
            int(contagem_anos['DATA STC'].max()),
            (int(contagem_anos['DATA STC'].min()), int(contagem_anos['DATA STC'].max()))
        )

        filtered_data = contagem_anos[
            (contagem_anos['DATA STC'] >= selected_years[0]) &
            (contagem_anos['DATA STC'] <= selected_years[1])
        ]

        fig = px.bar(
            filtered_data,
            x='DATA STC',
            y='CNPJ O',
            title='Números Anuais de Estabelecimentos Inativos na Cidade'
        )

        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Quantidade',
            title_x=0.2,
            title_font=dict(size=20),
            width=750,
            barmode='stack'
        )

        st.plotly_chart(fig)
    # FIM GRÁFICO 1


    # INICIO GRAFICO 2 - OK COM O FILTRO
    col1, col2 = st.columns([1, 4])  # Ajustei a proporção das colunas para centralizar
    with col2:
        contagem_atividades = df['CNAE PRINCP'].value_counts()

        # Número fixo de atividades no gráfico
        num_atividades_para_mostrar = 5
        top_atividades = contagem_atividades.nlargest(num_atividades_para_mostrar)
        outras_atividades = contagem_atividades.iloc[num_atividades_para_mostrar:]

        # Criar DataFrame para as 5 principais atividades
        top_df = pd.DataFrame({'Atividade': top_atividades.index, 'Frequência': top_atividades.values})

        # Criar gráfico de pizza para as 5 principais atividades
        fig = px.pie(top_df, values='Frequência', names='Atividade')

        fig.update_layout(
            title=f'Cenário Empresarial: As {num_atividades_para_mostrar} Atividades que Dominam a Economia Local',
            height=450,
            title_font=dict(size=20),
            title_x=0.08,
            width=800,
            legend=dict(orientation='h')
        )

        # Exibir gráfico no Streamlit
        st.plotly_chart(fig)

        # Controle de exibição da tabela
        if "mostrar_tabela" not in st.session_state:
            st.session_state.mostrar_tabela = False

        # Botão para "Ver outras atividades" (só aparece se a tabela não estiver visível)
        if not st.session_state.mostrar_tabela:
            if st.button("Ver outras atividades"):
                st.session_state.mostrar_tabela = True

        # Exibição condicional da tabela
        if st.session_state.mostrar_tabela:
            outras_df = pd.DataFrame({
                'Posição': range(num_atividades_para_mostrar + 1, num_atividades_para_mostrar + len(outras_atividades) + 1),
                'Atividade': outras_atividades.index,
                'Frequência': outras_atividades.values
            })

            st.markdown("### Outras Atividades Empresariais")

            # Exibir tabela com rolagem para melhorar a navegação
            st.dataframe(outras_df, height=300)  # A altura pode ser ajustada conforme necessário

            # Botão para "Fechar tabela" abaixo da tabela
            if st.button("Fechar tabela"):
                st.session_state.mostrar_tabela = False
                st.experimental_rerun()

    # INICIO GRAFICO 3 - inativos - OK COM O FILTRO
    col1, col2 = st.columns([1, 4])  # Ajustei a proporção das colunas para centralizar
    with col2:
        contagem_atividades_inativas = df_inativas['CNAE PRINCP'].value_counts()

        # Número fixo de atividades para mostrar no gráfico
        num_atividades_inativas_para_mostrar = 5  # Sempre exibir as 5 principais
        top_atividades_inativas = contagem_atividades_inativas.nlargest(num_atividades_inativas_para_mostrar)

        # Criar DataFrame com as atividades inativas mais frequentes
        top_df_inativas = pd.DataFrame({'Atividade': top_atividades_inativas.index, 'Frequência': top_atividades_inativas.values})
        top_df_inativas['Atividade'] = top_df_inativas['Atividade'].replace(
            {'Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns':'Comércio varejista de produtos alimentícios - minimercados e mercearias'}
        )

        # Criar gráfico de barras horizontais
        fig = px.bar(
            top_df_inativas, 
            x='Frequência', 
            y='Atividade', 
            orientation='h',
            labels={'Frequência': 'Encerramentos', 'Atividade': 'Atividade Econômica'},
            color='Frequência', 
            color_continuous_scale='reds',  # Gradiente de vermelho
            text='Frequência'  
        )

        # Configurações do gráfico
        fig.update_traces(hovertemplate='%{y}: %{x}')
        fig.update_layout(
            title=f'Tendências Econômicas: As {num_atividades_inativas_para_mostrar} Atividades mais Encerradas na Cidade',
            height=450,
            title_x=0.1,
            title_font=dict(size=20),
            width=800,
            coloraxis_colorbar=dict(title="Encerramentos"),
            xaxis_title="Quantidade de Encerramentos",
            yaxis_title=None,
            margin=dict(l=200) 
        )

        # Exibir gráfico
        st.plotly_chart(fig)

        # Controle de exibição da tabela
        if "mostrar_tabela_inativas" not in st.session_state:
            st.session_state.mostrar_tabela_inativas = False

        # Botão para "Ver outras atividades inativas"
        if not st.session_state.mostrar_tabela_inativas:
            if st.button("Ver outras atividades inativas"):
                st.session_state.mostrar_tabela_inativas = True

        # Exibição condicional da tabela
        if st.session_state.mostrar_tabela_inativas:
            outras_atividades_inativas = contagem_atividades_inativas.iloc[num_atividades_inativas_para_mostrar:]
            outras_df_inativas = pd.DataFrame({
                'Posição': range(num_atividades_inativas_para_mostrar + 1, num_atividades_inativas_para_mostrar + len(outras_atividades_inativas) + 1),
                'Atividade': outras_atividades_inativas.index,
                'Frequência': outras_atividades_inativas.values
            })

            st.markdown("### Outras Atividades Econômicas Inativas")

            # Exibir tabela com rolagem
            st.dataframe(outras_df_inativas, height=300)

            # Botão para "Fechar tabela inativas" abaixo da tabela
            if st.button("Fechar tabela inativas"):
                st.session_state.mostrar_tabela_inativas = False
                st.experimental_rerun()

    
    # Filtro estabelecimentos ativos pela atividade selecionada
    st.markdown("""
    <style>
    .font {
        font-size: 30px !important;
        margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font">Encontrando Estabelecimentos por Classificação de Atividades Econômicas (CNAE) 🏢 </h5>', unsafe_allow_html=True)

    st.markdown("""
    <style>
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
    </style>
    """, unsafe_allow_html=True)

    # Criar o container centralizado
    st.markdown('<div class="center-container">', unsafe_allow_html=True)

    selected_activity = st.selectbox("Selecione a atividade:", df['CNAE PRINCP'].unique())

    filtered_estabelecimentos = df[df['CNAE PRINCP'] == selected_activity]

    # Tabela de estabelecimentos filtrados
    table_data = filtered_estabelecimentos[['NOME FANT', 'BAIRRO']]
    table_data.columns = ['Nome do Estabelecimento', 'Bairro']
    table_data = table_data.reset_index(drop=True)

    # Estilo da tabela
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

    # Adicionar título para o gráfico de distribuição por bairro
    st.markdown("""
    <style>
    .font2 {
        font-size: 30px !important;
        margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<h5 class="font2">Distribuição por Bairro 📊 </h5>', unsafe_allow_html=True)

    # Calcular a distribuição por bairro
    total_estabelecimentos = len(filtered_estabelecimentos)
    bairro_counts = filtered_estabelecimentos['BAIRRO'].value_counts()
    bairro_counts_df = pd.DataFrame({'Bairro': bairro_counts.index, 'Contagem': bairro_counts.values})
    st.write(f" 🔵 Total de Estabelecimentos: {total_estabelecimentos}")

    # Criar gráfico de barras para distribuição por bairro
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
