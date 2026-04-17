import streamlit as st
import pandas as pd
from plotly import graph_objs as go
import plotly.express as px
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from PIL import Image

# --- Configurações Iniciais da Página ---
st.set_page_config(
    page_title="Cedro Localize",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- CSS Global para Estilização da Interface ---
st.markdown("""
<style>
    /* Estilo geral */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
        background-color: #f0f2f6; 
    }

    /* Títulos principais da página */
    h1 {
        color: #2c3e50; 
        font-size: 2.5em; 
        margin-bottom: 0.5em;
    }
    h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }

    /* Sidebar */
    .css-1d391kg, .css-1dp5vir { 
        background-color: #f0f2f6; 
        padding: 10px;
        border-right: 1px solid #e0e4eb;
    }
    .st-emotion-cache-1kyx2bd, .st-emotion-cache-1wivc8r { /* Título do menu na sidebar */
        color: #2c3e50;
    }

    .big-number-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        text-align: center;
    }
    .big-number {
        font-size: 60px; 
        font-weight: bold;
        color: #4A90E2; 
        margin-bottom: 5px;
    }
    .big-number-label {
        font-size: 24px;
        color: #555;
    }

    /* Estilo para os cards de métricas (st.info, st.warning, st.success) */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .stAlert > div > svg { /* Ícones dentro dos alerts */
        color: #ffffff !important;
    }
    .stAlert.info { background-color: #4A90E2; color: white; } 
    .stAlert.info strong { color: white; }
    .stAlert.warning { background-color: #f7b731; color: white; } 
    .stAlert.warning strong { color: white; }
    .stAlert.success { background-color: #2ecc71; color: white; } 
    .stAlert.success strong { color: white; }
    .stAlert p { margin-bottom: 5px; } 

    /* Estilo para tabelas de dados (st.dataframe) */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* Estilo para caixas de informações (nos detalhes do estabelecimento na busca) */
    .info-box {
        background-color: #e0e4eb; 
        padding: 15px;
        border-left: 5px solid #4A90E2; 
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .info-box p {
        margin: 5px 0;
    }

    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .streamlit-expanderContent {
        background-color: #f8f9fa;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        padding: 15px;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .css-1dp5vir .menu-list ul li a svg {
        fill: #4A90E2 !important; 
    }
    .css-1dp5vir .menu-list ul li .nav-link-selected svg {
        fill: white !important;
    }
    .st-emotion-cache-1wivc8r { /* Título do menu na sidebar */
        margin-top: -10px; 
        margin-bottom: 5px; 
    }
    .st-emotion-cache-vk33c6, .st-emotion-cache-1d391kg { /* Classes que podem controlar o padding da sidebar */
        padding-top: 0rem;
    }

    .st-emotion-cache-16txt4v { /* Classe que envolve a imagem e o menu */
        margin-top: -40px; 
    }


</style>
""", unsafe_allow_html=True)

# --- Carregamento de Dados ---
try:
    df = pd.read_csv('estabcnaeok.csv', index_col=False)
    df_inativas = pd.read_csv('estab_inativos_ok.csv')
    dfloc = pd.read_csv('estabGeolocalizadoOK.csv')

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df_inativas = df_inativas.loc[:, ~df_inativas.columns.str.contains('^Unnamed')]
except FileNotFoundError:
    st.error("Erro: Verifique se os arquivos CSV ('estabcnaeok.csv', 'estab_inativos_ok.csv', 'estabGeolocalizadoOK.csv') estão no mesmo diretório da aplicação.")
    st.stop()



# Conversão de colunas de data para datetime
df['DATA STC'] = pd.to_datetime(df['DATA STC'], errors='coerce')
df_inativas['DATA STC'] = pd.to_datetime(df_inativas['DATA STC'], errors='coerce')
# Garantir que as colunas de Latitude e Longitude são numéricas no dfloc
dfloc['Latitude'] = pd.to_numeric(dfloc['Latitude'], errors='coerce')
dfloc['Longitude'] = pd.to_numeric(dfloc['Longitude'], errors='coerce')
dfloc.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# --- Sidebar com Option Menu ---
with st.sidebar:

    choose = option_menu(
        menu_title="Menu de Navegação",
        options=["Sobre", "Estabelecimentos", "Localizações"],
        icons=['house-door-fill', 'building-fill', 'geo-alt-fill'],
        default_index=0,    
        styles={
            # Container do menu
            "container": {
                "padding": "0!important", 
                "background-color": "#F5F5F5", 
                "border-radius": "8px"
            },
            "icon": {
                "font-size": "18px",
                "margin-right": "10px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin":"5px 0px",
                "padding": "10px 15px",
                "--hover-color": "#e0e4eb",
                "border-radius": "5px",
                "color": "#333333" 
            },
            "nav-link-selected": {
                "background-color": "#4A90E2", 
                "color": "white",
                "font-weight": "600",
            },
            
        }
    )

# --- Conteúdo das Páginas ---
if choose == "Estabelecimentos":
    st.title("📊 Painel de Estabelecimentos")
    st.markdown("---")

    # --- Cards de Métricas ---
    st.markdown("### Visão Geral dos Estabelecimentos")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**Total de Estabelecimentos Ativos**\n\n# {df.shape[0]}", icon="✅")
    with col2:
        st.warning(f"**Total de Estabelecimentos Inativos**\n\n# {df_inativas.shape[0]}", icon="❌")
    with col3:
        if not df.empty:
            ano_mais_aberturas = df['DATA STC'].dt.year.value_counts().idxmax()
            st.success(f"**Ano com Mais Aberturas**\n\n# {ano_mais_aberturas}", icon="📈")
        else:
            st.success(f"**Ano com Mais Aberturas**\n\n# N/A", icon="📈")

    st.markdown("---")

    # --- Gráficos de Tendência (Ativos e Inativos) ---

    df['DT IN ATV'] = pd.to_datetime(df['DT IN ATV'], dayfirst=True, errors='coerce')
    df_inativas['DATA STC'] = pd.to_datetime(df_inativas['DATA STC'], dayfirst=True, errors='coerce')

    st.markdown("### Dinâmica de Abertura e Encerramento ao Longo do Tempo")
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.subheader("Estabelecimentos Ativos por Ano")
        
        df_ativos_count = df.copy()
        df_ativos_count['Ano'] = df_ativos_count['DT IN ATV'].dt.year
        df_ativos_count = df_ativos_count.dropna(subset=['Ano'])
        
        contagem_anos_ativos = df_ativos_count.groupby('Ano')['CNPJ O'].count().reset_index()
        contagem_anos_ativos.columns = ['Ano', 'Quantidade']
        
        if not contagem_anos_ativos.empty:
            min_y, max_y = int(contagem_anos_ativos['Ano'].min()), int(contagem_anos_ativos['Ano'].max())
            
            selected_years = st.slider("Intervalo (Ativos)", min_y, max_y, (min_y, max_y), key="s1")
            
            # Filtrar
            filtered = contagem_anos_ativos[
                (contagem_anos_ativos['Ano'] >= selected_years[0]) & 
                (contagem_anos_ativos['Ano'] <= selected_years[1])
            ].copy()
            
            if not filtered.empty:
                chart_data = filtered.set_index('Ano')['Quantidade']
                st.bar_chart(chart_data, color="#636EFA")
            else:
                st.warning("Sem dados para o filtro selecionado.")
        else:
            st.error("Coluna 'DT IN ATV' está vazia após conversão.")

    with col_graph2:
        st.subheader("Estabelecimentos Inativos por Ano")
        
        df_inativos_count = df_inativas.copy()
        df_inativos_count['Ano'] = df_inativos_count['DATA STC'].dt.year
        df_inativos_count = df_inativos_count.dropna(subset=['Ano'])
        
        contagem_anos_inativos = df_inativos_count.groupby('Ano')['CNPJ O'].count().reset_index()
        contagem_anos_inativos.columns = ['Ano', 'Quantidade']
        
        if not contagem_anos_inativos.empty:
            min_y_in, max_y_in = int(contagem_anos_inativos['Ano'].min()), int(contagem_anos_inativos['Ano'].max())
            
            selected_years_in = st.slider("Intervalo (Inativos)", min_y_in, max_y_in, (min_y_in, max_y_in), key="s2")
            
            filtered_in = contagem_anos_inativos[
                (contagem_anos_inativos['Ano'] >= selected_years_in[0]) & 
                (contagem_anos_inativos['Ano'] <= selected_years_in[1])
            ].copy()
            
            if not filtered_in.empty:
                chart_data_in = filtered_in.set_index('Ano')['Quantidade']
                st.bar_chart(chart_data_in, color="#EF553B")
            else:
                st.warning("Sem dados para o filtro selecionado.")

    st.markdown("---")

    # --- Análise por Atividade Econômica (Ativas e Inativas) ---
    st.markdown("### Análise por Classificação de Atividades Econômicas (CNAE)")
    
    # Gráfico de Atividades Econômicas Ativas
    st.subheader("Top Atividades Econômicas Ativas")
    num_atividades_para_mostrar = st.slider("Selecione o número de atividades ", 3, 15, 5, key="top_ativos_slider")
    contagem_atividades = df['CNAE PRINCP'].value_counts()
    top_atividades = contagem_atividades.nlargest(num_atividades_para_mostrar).reset_index()
    top_atividades.columns = ['Atividade', 'Frequência']

    fig_pie = px.pie(top_atividades, values='Frequência', names='Atividade',
                     title=f'As {num_atividades_para_mostrar} Atividades que Dominam a Economia Local',
                     hole=0.3, 
                     color_discrete_sequence=px.colors.qualitative.Light24) 
    fig_pie.update_layout(
        height=550, 
        title_x=0, 
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=100, l=0, r=0), 
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.3,
            xanchor="center", 
            x=0.5,
            font=dict(size=10), 
        )
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Lógica da tabela detalhada para atividades ativas
    if 'show_table_ativos' not in st.session_state:
        st.session_state.show_table_ativos = False

    if st.button("Ver Tabela Detalhada de Atividades Ativas", key="btn_tabela_ativos_show"):
        st.session_state.show_table_ativos = True

    if st.session_state.show_table_ativos:
        st.dataframe(contagem_atividades.reset_index().rename(columns={'index': 'Atividade', 'CNAE PRINCP': 'Atividade'}),
                      use_container_width=True)
        if st.button("Fechar Tabela de Atividades Ativas", key="btn_tabela_ativos_hide"):
            st.session_state.show_table_ativos = False

    st.markdown("---") 

    # Gráfico de Atividades Econômicas Encerradas
    st.subheader("Top Atividades Econômicas Encerradas")
    num_atividades_inativas_para_mostrar = st.slider("Selecione o número de atividades ", 3, 15, 5, key="top_inativos_slider")
    contagem_atividades_inativas = df_inativas['CNAE PRINCP'].value_counts()
    top_atividades_inativas = contagem_atividades_inativas.nlargest(num_atividades_inativas_para_mostrar).reset_index()
    top_atividades_inativas.columns = ['Atividade', 'Frequência']

    fig_bar_inativas = px.bar(top_atividades_inativas, x='Frequência', y='Atividade', orientation='h',
                              title=f'As {num_atividades_inativas_para_mostrar} Atividades mais Encerradas na Cidade',
                              color='Frequência', color_continuous_scale='Reds',
                              text='Frequência',
                              template='plotly_white')
    fig_bar_inativas.update_layout(
        height=450, 
        title_x=0, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Quantidade de Encerramentos", 
        yaxis_title=None,
        yaxis={'categoryorder':'total ascending'},
        margin=dict(l=200, r=20, t=50, b=20)
    )
    fig_bar_inativas.update_traces(texttemplate='%{x}', textposition='outside')
    st.plotly_chart(fig_bar_inativas, use_container_width=True)

    # Lógica da tabela detalhada para atividades inativas
    if 'show_table_inativas' not in st.session_state:
        st.session_state.show_table_inativas = False

    if st.button("Ver Tabela Detalhada de Atividades Encerradas", key="btn_tabela_inativas_show"):
        st.session_state.show_table_inativas = True

    if st.session_state.show_table_inativas:
        st.dataframe(contagem_atividades_inativas.reset_index().rename(columns={'index': 'Atividade', 'CNAE PRINCP': 'Atividade'}),
                      use_container_width=True)
        if st.button("Fechar Tabela de Atividades Encerradas", key="btn_tabela_inativas_hide"):
            st.session_state.show_table_inativas = False

    st.markdown("---")

    # --- Busca e Filtragem de Estabelecimentos por Atividade ---
    st.markdown("### Encontrando Estabelecimentos por Atividade Econômica")
    
    selected_activity_filter = st.selectbox(
        "Selecione a atividade para filtrar estabelecimentos:",
        options=['Todas'] + sorted(df['CNAE PRINCP'].unique().tolist()),
        key="select_activity_filter"
    )

    if selected_activity_filter == 'Todas':
        filtered_estabelecimentos = df
    else:
        filtered_estabelecimentos = df[df['CNAE PRINCP'] == selected_activity_filter]

    st.info(f"🔵 **Total de Estabelecimentos encontrados:** {len(filtered_estabelecimentos)}")

    st.dataframe(filtered_estabelecimentos[['NOME FANT', 'BAIRRO', 'LOGRD', 'DT IN ATV', 'CNAE PRINCP']].rename(columns={
        'NOME FANT': 'Nome do Estabelecimento',
        'BAIRRO': 'Bairro',
        'LOGRD': 'Endereço',
        'DT IN ATV': 'Data de Início',
        'CNAE PRINCP': 'CNAE Principal'
    }), use_container_width=True, height=350)

    if not filtered_estabelecimentos.empty:
        st.subheader(f"Distribuição de Estabelecimentos por Bairro (Atividade: {selected_activity_filter})")
        bairro_counts = filtered_estabelecimentos['BAIRRO'].value_counts().reset_index()
        bairro_counts.columns = ['Bairro', 'Contagem']
        
        fig_bairro = px.bar(bairro_counts, x='Bairro', y='Contagem',
                            title='Distribuição por Bairro da Atividade Selecionada',
                            color_discrete_sequence=px.colors.qualitative.Vivid,
                            template='plotly_white')
        fig_bairro.update_layout(height=400, title_x=0, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bairro, use_container_width=True)
    else:
        st.info("Nenhum estabelecimento encontrado para a atividade selecionada para mostrar a distribuição por bairro.")


elif choose == "Localizações":
    st.title("📍 Localização de Estabelecimentos")
    st.markdown("---")

    # --- Busca por Estabelecimento Específico ---
    st.markdown("### Busca Detalhada por Estabelecimento")
    name_local = st.text_input(label='Digite o nome do estabelecimento para buscar:',
                               placeholder='Ex: Mercadinho Boa Esperança',
                               key="search_input_local")

    if name_local:
        filter_local = df[df['NOME FANT'].str.contains(name_local, case=False, na=False)]
        
        if not filter_local.empty:
            st.markdown("#### Resultados da Busca:")
            for i, row in filter_local.iterrows():
                with st.expander(f"Detalhes de {row['NOME FANT']}"):
                    st.markdown(f"""
                        <div class="info-box">
                            <p><strong>Nome Fantasia:</strong> {row['NOME FANT']}</p>
                            <p><strong>Data de Início da Atividade:</strong> {row['DT IN ATV']}</p>
                            <p><strong>Endereço:</strong> {row['LOGRD']}, {row['NUMERO']} - {row['BAIRRO']}, {row['MUNICIPIO']}</p>
                            <p><strong>CEP:</strong> {row['CEP']}</p>
                            <p><strong>CNAE Principal:</strong> {row['CNAE PRINCP']}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.error('Nenhum estabelecimento encontrado com esse nome.')
    else:
        st.info("Digite um nome no campo acima para buscar informações sobre estabelecimentos e seus detalhes.")

    st.markdown("---")
        # --- Mapa de Distribuição dos Estabelecimentos ---
    st.markdown("### Distribuição Geográfica dos Estabelecimentos")
    st.markdown("Visualize a dispersão geográfica de todos os estabelecimentos geolocalizados na cidade.")

    dfloc_brasil = pd.DataFrame()

    if not dfloc.empty:
        dfloc_brasil = dfloc[
            (dfloc['Latitude'].between(-35.0, 5.0)) &
            (dfloc['Longitude'].between(-75.0, -30.0))
        ]

        dfloc_brasil['Latitude'] = pd.to_numeric(dfloc_brasil['Latitude'], errors='coerce')
        dfloc_brasil['Longitude'] = pd.to_numeric(dfloc_brasil['Longitude'], errors='coerce')
        dfloc_brasil = dfloc_brasil.dropna(subset=['Latitude', 'Longitude'])

    if not dfloc_brasil.empty:
        center_lat = float(dfloc_brasil['Latitude'].mean())
        center_lon = float(dfloc_brasil['Longitude'].mean())

        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in dfloc_brasil.iterrows():
            nome = str(row['NOME FANT']) if pd.notna(row['NOME FANT']) else "Sem nome"
            bairro = str(row['BAIRRO']) if pd.notna(row['BAIRRO']) else "Sem bairro"

            folium.Marker(
                location=[float(row['Latitude']), float(row['Longitude'])],
                popup=f"<b>{nome}</b><br>Bairro: {bairro}",
                tooltip=nome
            ).add_to(marker_cluster)

        st_folium(m, width=900, height=500)

    else:
        st.warning("Nenhum ponto com coordenadas válidas no Brasil foi encontrado.")


elif choose == "Sobre":
    st.title("💡 Sobre o Cedro Localize")
    st.markdown("---")
    col_about1, col_about2 = st.columns([1, 1])

    with col_about1:
        st.markdown("""

        O **Cedro Localize** é um projeto de TCC desenvolvido para o curso de **Sistemas de Informação do IFCE - Campus Cedro**.

        Esta ferramenta busca contribuir para a **democratização do acesso aos dados** locais, permitindo que qualquer pessoa entenda o panorama geral do cenário empresarial da cidade de forma simples e visual.

        **Nota:** As informações e tendências apresentadas utilizam dados coletados até o ano de **2023**.
        """)
    with col_about2:
        st.image("1111.jpg",
                  caption="Uma visão detalhada do cenário empresarial de Cedro, CE (Dados até 2023). ")
        st.markdown("""
            **Desenvolvido por:** Géssica Pereira da Silva
            <br>
            **Instituição:** IFCE Campus Cedro
        """, unsafe_allow_html=True)