# -*- coding: utf-8 -*-
"""
=============================================================================
CLEANQUERY - STREAMLIT WEB APP
=============================================================================
Este arquivo implementa a versão oficial interativa em Streamlit do
Social Media Query Creator. Oferece o mesmo visual sofisticado e o fluxo
completo da aplicação React, incluindo colagem de links e upload de arquivos.
=============================================================================
"""

import streamlit as st
import pandas as pd
import re
from urllib.parse import urlparse, parse_qs
import io

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Social Media Query Creator - Burson",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para refletir o luxuoso design corporativo Burson (Slate escuro, amarelo brilhante e off-white)
st.markdown("""
<style>
    /* Configurações Gerais de Fundo e Layout */
    .stApp {
        background-color: #FFFFF1;
    }
    
    /* Fontes e Cabeçalhos corporativos */
    h1, h2, h3, .brand-title {
        color: #0A0400 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    .brand-title {
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: -1.2px;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
        border-bottom: 3px solid #FEFF00;
        display: inline-block;
        padding-bottom: 0.2rem;
    }
    
    .brand-subtitle {
        color: #555c68;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 1.8rem;
    }
    
    /* Estilização de Cartões de Métricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e1e8f0;
        border-left: 5px solid #0A0400;
        border-radius: 6px;
        padding: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.01);
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 900;
        color: #0A0400;
        margin: 0;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 0.6px;
        margin-top: 0.3rem;
    }
    
    /* Customização dos botões e alertas do Streamlit */
    div.stButton > button {
        background-color: #0A0400 !important;
        color: #FEFF00 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1.25rem !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button:hover {
        background-color: #222222 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# SAMPLE DATA SET EXACTLY REPLICATING /src/data.ts
SAMPLE_ROWS = [
    {
        'Data': '29/05/2026',
        'Canal': 'Facebook',
        'Autor': 'Ana Silva',
        'URL': 'https://www.facebook.com/703877341748998/posts/1459573502846041',
        'Sentimento': 'Negativo',
        'Tags': 'Crise, Atendimento'
    },
    {
        'Data': '29/05/2026',
        'Canal': 'Twitter/X',
        'Autor': 'Estadão E-Investidor',
        'URL': 'http://twitter.com/EInvestidor/status/2036442951404933226',
        'Sentimento': 'Negativo',
        'Tags': 'Crise, Mercado'
    },
    {
        'Data': '28/05/2026',
        'Canal': 'Instagram',
        'Autor': 'Felipe Santos',
        'URL': 'https://www.instagram.com/p/C7X3x1uuW8z/',
        'Sentimento': 'Positivo',
        'Tags': 'Campanha, Influenciador'
    },
    {
        'Data': '28/05/2026',
        'Canal': 'Instagram',
        'Autor': 'Mariana Souza',
        'URL': 'https://www.instagram.com/reel/C8AbCdEfGhI/',
        'Sentimento': 'Negativo',
        'Tags': 'Reclamação, Qualidade'
    },
    {
        'Data': '27/05/2026',
        'Canal': 'TikTok',
        'Autor': 'Estadão Notícias',
        'URL': 'https://www.tiktok.com/@estadao/video/7352345678912345678',
        'Sentimento': 'Negativo',
        'Tags': 'Crise, Marcas'
    },
    {
        'Data': '26/05/2026',
        'Canal': 'YouTube',
        'Autor': 'Canal Tech News',
        'URL': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'Sentimento': 'Neutro',
        'Tags': 'Review, Informativo'
    },
    {
        'Data': '26/05/2026',
        'Canal': 'Twitter/X',
        'Autor': 'Gabriel Pace',
        'URL': 'https://x.com/GloboNews/status/1789234567891234567',
        'Sentimento': 'Negativo',
        'Tags': 'Política'
    },
    {
        'Data': '25/05/2026',
        'Canal': 'Notícias',
        'Autor': 'G1 Globo',
        'URL': 'https://g1.globo.com/politica/noticia/2026/05/29/materia.html',
        'Sentimento': 'Neutro',
        'Tags': 'Imprensa'
    },
    {
        'Data': '24/05/2026',
        'Canal': 'LinkedIn',
        'Autor': 'Executivo Exemplo',
        'URL': 'https://www.linkedin.com/feed/update/urn:li:activity:7123456789123456789/',
        'Sentimento': 'Positivo',
        'Tags': 'Institucional'
    },
    {
        'Data': '24/05/2026',
        'Canal': 'LinkedIn',
        'Autor': 'Especialista Burson',
        'URL': 'https://www.linkedin.com/posts/gabriel-pace-123456',
        'Sentimento': 'Neutro',
        'Tags': 'Comunicação'
    },
    {
        'Data': '23/05/2026',
        'Canal': 'Instagram',
        'Autor': 'Itatiaia Oficial',
        'URL': 'https://www.instagram.com/itatiaiaoficial/p/DVbUsaklPnE/',
        'Sentimento': 'Negativo',
        'Tags': 'Rádio, Notícias'
    },
    {
        'Data': '22/05/2026',
        'Canal': 'Facebook',
        'Autor': 'Rádio Itatiaia',
        'URL': 'https://www.facebook.com/radioitatiaia/posts/amazon-conecta-2026-re%C3%BAne-15-mil-vendedores-para-capacita%C3%A7%C3%A3o-em-s%C3%A3o-pauloclique-/1468483525305135/',
        'Sentimento': 'Negativo',
        'Tags': 'Rádio, Patrocínio'
    }
]

# =============================================================================
# EXTRACTOR CORE LOGIC (Python matching /src/utils/urlParser.ts exactly)
# =============================================================================
def extrair_id_da_url(url: str, active_platforms: dict) -> tuple:
    """
    Analisa e extrai o ID correspondente da publicação dependendo da plataforma.
    Retorna (id_extraido, nome_plataforma, is_valid)
    """
    if not isinstance(url, str) or not url.strip():
        return "", "others", False

    trimmed = url.strip()

    # 1. Twitter / X
    if ("twitter.com" in trimmed or "x.com" in trimmed) and active_platforms.get('twitter', True):
        # Padrão original de status
        twitter_regex = r'(?:twitter\.com|x\.com)/[^/]+/status/(\d+)'
        match = re.search(twitter_regex, trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'twitter', True
            
        # Fallback de ID numérico no final da rota
        fallback_match = re.search(r'/(\d+)/?(?:\?|$)', trimmed)
        if fallback_match:
            return fallback_match.group(1), 'twitter', True

    # 2. Facebook
    elif "facebook.com" in trimmed and active_platforms.get('facebook', True):
        # Primeiro, tentar extrair número grande de ID no final da URL
        normalized_url = trimmed.rstrip('/')
        match_end_num = re.search(r'/(\d{6,25})(?:\?|#|$)', normalized_url)
        if match_end_num:
            return match_end_num.group(1), 'facebook', True

        # Padrão posts normais
        posts_regex = r'/posts/(\d+)'
        match = re.search(posts_regex, trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'facebook', True

        # Permalink de grupo
        groups_regex = r'/permalink/(\d+)'
        match_perm = re.search(groups_regex, trimmed, re.IGNORECASE)
        if match_perm:
            return match_perm.group(1), 'facebook', True

        # Parâmetro de URL query
        try:
            parsed = urlparse(trimmed)
            qs = parse_qs(parsed.query)
            for param in ['story_fbid', 'fbid', 'id']:
                if param in qs and qs[param]:
                    val = qs[param][0]
                    if re.match(r'^\w+$', val):
                        return val, 'facebook', True
        except Exception:
            pass

        # Padrão genérico de posts que pode ter um slug com traço
        match_gen = re.search(r'/posts/([^/?]+)', trimmed, re.IGNORECASE)
        if match_gen:
            id_only = match_gen.group(1).split('?')[0]
            has_word_hyphens = id_only.count('-') > 2
            is_plain_word = re.match(r'^[A-Za-z_-]+$', id_only) and len(id_only) > 5
            if not has_word_hyphens and not is_plain_word:
                return id_only, 'facebook', True

    # 3. Instagram
    elif "instagram.com" in trimmed and active_platforms.get('instagram', True):
        # Padrão direto
        match_direct = re.search(r'instagram\.com/(?:p|reel|tv)/([^/?]+)', trimmed, re.IGNORECASE)
        if match_direct:
            return match_direct.group(1), 'instagram', True
            
        # Padrão com o nome do perfil
        match_user = re.search(r'instagram\.com/[^/]+/(?:p|reel|tv)/([^/?]+)', trimmed, re.IGNORECASE)
        if match_user:
            return match_user.group(1), 'instagram', True

    # 4. TikTok
    elif "tiktok.com" in trimmed and active_platforms.get('tiktok', True):
        match = re.search(r'tiktok\.com/@[^/]+/video/(\d+)', trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'tiktok', True
            
        short_match = re.search(r'tiktok\.com/t/([^/?]+)', trimmed, re.IGNORECASE) or re.search(r'vm\.tiktok\.com/([^/?]+)', trimmed, re.IGNORECASE)
        if short_match:
            return short_match.group(1), 'tiktok', True

    # 5. YouTube
    elif ("youtube.com" in trimmed or "youtu.be" in trimmed) and active_platforms.get('youtube', True):
        match = re.search(r'v=([^&#?]+)', trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'youtube', True
            
        short_match = re.search(r'youtu\.be/([^/?]+)', trimmed, re.IGNORECASE)
        if short_match:
            return short_match.group(1), 'youtube', True

    # 6. LinkedIn
    elif "linkedin.com" in trimmed and active_platforms.get('linkedin', True):
        match = re.search(r'urn:li:activity:(\d+)', trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'linkedin', True
            
        fallback_match = re.search(r'/(\d+)/?(?:\?|$)', trimmed)
        if fallback_match:
            return fallback_match.group(1), 'linkedin', True

    # Robust Fallback genérico para links estruturados
    try:
        # 1. Verifica se tem sequência numérica marcante no fim do caminho
        end_numeric_match = re.search(r'/(\d{6,25})/?(?:\?|#|$)', trimmed)
        if end_numeric_match:
            return end_numeric_match.group(1), 'others', True

        # 2. Sequência numérica longa no meio (8+ dígitos)
        body_numeric_match = re.search(r'(?:^|/|\D)(\d{8,25})(?:\D|$)', trimmed)
        if body_numeric_match:
            return body_numeric_match.group(1), 'others', True

        # 3. Bloco alfa numérico final sanitizado
        cleaned = trimmed.rstrip('/')
        segments = cleaned.split('/')
        if segments:
            last_segment = segments[-1].split('?')[0]
            has_word_hyphens = last_segment.count('-') > 2
            is_clean_code = re.match(r'^[A-Za-z0-9_-]{4,25}$', last_segment)
            is_plain_word = re.match(r'^[A-Za-z_-]+$', last_segment) and len(last_segment) > 5
            
            if is_clean_code and not has_word_hyphens and not is_plain_word:
                return last_segment, 'others', True
    except Exception:
        pass

    return "", "others", False


# =============================================================================
# LAYOUT & INTERFACE DO USUÁRIO STREAMLIT
# =============================================================================

st.markdown('<div class="brand-title">🔍 BURSON QUERY GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">Extrator de IDs Higienizados & Gerador de Query Booleana com Limitador de 4096 Caracteres</div>', unsafe_allow_html=True)

# Divisão de Colunas: Barra Lateral de Configurações & Painel Principal
with st.sidebar:
    st.markdown("### 🛠️ CONFIGURAÇÕES ")
    
    # 1. Escolha do Método de Entrada dos Dados (Exatamente igual ao React)
    input_method = st.radio(
        "Selecione o método de entrada:",
        ["Colar links diretamente (Mais rápido)", "Carregar planilha .xlsx / .csv", "Testar com dados de exemplo"],
        index=0
    )
    
    st.write("---")
    
    # 2. Seleção de Redes Sociais Ativas (Multi-toggles)
    st.markdown("**🌐 Canais Ativos para Monitorizar**")
    active_twitter = st.toggle("Twitter / X", value=True)
    active_facebook = st.toggle("Facebook", value=True)
    active_instagram = st.toggle("Instagram", value=True)
    active_tiktok = st.toggle("TikTok", value=True)
    active_youtube = st.toggle("YouTube", value=True)
    active_linkedin = st.toggle("LinkedIn", value=True)
    
    active_platforms = {
        'twitter': active_twitter,
        'facebook': active_facebook,
        'instagram': active_instagram,
        'tiktok': active_tiktok,
        'youtube': active_youtube,
        'linkedin': active_linkedin
    }
    
    st.write("---")
    
    # 3. Remover LinkedIn preventivamente (recurso do App React)
    remove_linkedin_preemptive = st.checkbox("Remover links do LinkedIn", value=True, 
                                            help="Quando marcado, descarta links de 'linkedin.com' automaticamente para diminuir o tamanho final da query.")

    # 4. Bloco de ajuda para o Deploy no Streamlit Cloud
    st.write("---")
    with st.expander("🚀 Como publicar este app no seu GitHub?", expanded=False):
        st.markdown("""
        **Passo a passo simples:**
        1. Crie uma conta gratuita em [github.com](https://github.com) se não tiver.
        2. No canto superior direito, clique em **New Repository**.
        3. Dê o nome de **`cleanquery-burson`** e marque como **Public**.
        4. Suba ou crie os seguintes arquivos na raiz do repo:
           - **`app.py`** (este mesmo arquivo)
           - **`requirements.txt`** (contendo as bibliotecas necessárias)
        5. Vá em [share.streamlit.io](https://share.streamlit.io), conecte seu GitHub e selecione este repositório.
        6. Clique em **Deploy** e seu app estará no ar para qualquer colega usar!
        """)

# Inicializar os dados de acordo com o método de entrada escolhido
df_origin = None
url_column = "URL"
use_filter = False
filter_column = ""
filter_value = ""

if input_method == "Colar links diretamente (Mais rápido)":
    st.markdown("### 📋 1. Cole seus links de redes sociais")
    paste_content = st.text_area(
        "Insira os links brutos (cole as linhas da coluna do Excel diretamente aqui, um link por linha):",
        value="",
        placeholder="https://www.facebook.com/703877341748998/posts/1459573502846041\nhttps://twitter.com/EInvestidor/status/2036442951404933226\nhttps://www.instagram.com/p/C7X3x1uuW8z/",
        height=180
    )
    
    if paste_content.strip():
        # Converter linhas coladas em DataFrame
        lines = [line.strip() for line in paste_content.split('\n') if line.strip()]
        df_origin = pd.DataFrame({'URL': lines})
        url_column = 'URL'
    else:
        st.info("👆 Cole alguns links de publicação acima para ver os IDs sendo extraídos instantaneamente!")

elif input_method == "Carregar planilha .xlsx / .csv":
    st.markdown("### 📁 1. Faça upload da planilha Excel ou CSV")
    uploaded_file = st.file_uploader(
        "Carregue seu relatório ou planilha (.xlsx ou .csv):",
        type=["xlsx", "xls", "csv"],
        help="A planilha deve ter uma coluna de links/URLs de redes sociais."
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_origin = pd.read_csv(uploaded_file)
            else:
                df_origin = pd.read_excel(uploaded_file, engine='openpyxl')
                
            st.toast("⚡ Planilha carregada e lida com sucesso!", icon="✅")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo selecionado: {e}")
            df_origin = None
            
    if df_origin is not None:
        # Configurações de coluna de URLs
        cols = list(df_origin.columns)
        
        # Tentar auto-identificar coluna 'URL'
        url_idx = 0
        for i, col in enumerate(cols):
            if col.lower() in ['url', 'link', 'mencion', 'menção', 'endereco', 'endereço']:
                url_idx = i
                break
                
        # Layout lado a lado para mapear as colunas
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            url_column = st.selectbox("Selecione a coluna de URLs:", options=cols, index=url_idx)
            
        with col_c2:
            use_filter = st.checkbox("Aplicar filtro de coluna (ex: Sentimento = Negativo)", value=False)
            
        if use_filter:
            # Mapear coluna de sentimento/filtragem
            filter_idx = 0
            for i, col in enumerate(cols):
                if col.lower() in ['sentimento', 'sentiment', 'tag', 'status']:
                    filter_idx = i
                    break
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filter_column = st.selectbox("Filtrar pela coluna:", options=cols, index=filter_idx)
            with col_f2:
                filter_value = st.text_input("Contendo o valor:", value="Negativo")
    else:
        st.info("💡 Faça o upload de uma planilha para selecionar as colunas de URLs e configurar os filtros.")

else: # Usar dados de exemplo
    st.markdown("### 💡 1. Testando com dados de simulação Burson")
    df_origin = pd.DataFrame(SAMPLE_ROWS)
    url_column = 'URL'
    
    # Adicionar configuração de filtros padrão para que use como exemplo
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.info("Usando coluna padrão de links: **'URL'**.")
    with col_c2:
        use_filter = st.checkbox("Filtrar por sentimento na simulação", value=True)
        
    if use_filter:
        filter_column = 'Sentimento'
        filter_value = 'Negativo'
        st.caption("Filtro Ativo: `Sentimento = Negativo`")


# =============================================================================
# EXECUTAR FILTRAGEM & EXTRAÇÃO DE IDs
# =============================================================================
if df_origin is not None:
    # 1. Aplicar filtro preemptivo se configurado
    df_working = df_origin.copy()
    
    # Se configurado para remover linkedin de forma preemptiva na varredura geral
    if remove_linkedin_preemptive and url_column in df_working.columns:
        # Filtrar fora links do linkedin
        df_working = df_working[~df_working[url_column].astype(str).str.lower().str.contains('linkedin', na=False)]
        
    if use_filter and filter_column:
        df_working = df_working[df_working[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
        
    # 2. Executar extração linha a linha
    rows_processed = []
    ids_unicos = []
    
    for idx, row in df_working.iterrows():
        url_val = str(row.get(url_column, "")).strip()
        
        if not url_val or url_val.lower() == 'nan':
            continue
            
        post_id, platform, is_valid = extrair_id_da_url(url_val, active_platforms)
        
        status = "Sucesso" if is_valid else "Não identificado/Bloqueado"
        
        rows_processed.append({
            'URL_Original': url_val,
            'ID_Extraido': post_id if is_valid else "",
            'Canal': platform.capitalize() if platform != 'others' else 'Outros',
            'Resultado': status,
            'Valido': is_valid,
            'Info': row.to_dict() # manter os metadados
        })
        
        if is_valid and post_id not in ids_unicos:
            ids_unicos.append(post_id)
            
    df_results_full = pd.DataFrame(rows_processed)
    
    # 3. Exibir Cartões de Métricas no topo dos Resultados
    st.write("---")
    st.markdown("### 📊 2. Métricas do Batch Processado")
    
    total_linhas_iniciais = len(df_origin)
    total_linhas_filtradas = len(df_working)
    total_sucesso = len(df_results_full[df_results_full['Valido'] == True]) if len(df_results_full) > 0 else 0
    total_ids_unicos = len(ids_unicos)
    
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    with met_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{total_linhas_iniciais}</div>
            <div class="metric-label">Linhas Totais</div>
        </div>
        """, unsafe_allow_html=True)
    with met_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{total_linhas_filtradas}</div>
            <div class="metric-label">Linhas Selecionadas</div>
        </div>
        """, unsafe_allow_html=True)
    with met_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{total_sucesso}</div>
            <div class="metric-label">IDs Extraídos</div>
        </div>
        """, unsafe_allow_html=True)
    with met_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{total_ids_unicos}</div>
            <div class="metric-label">IDs Únicos</div>
        </div>
        """, unsafe_allow_html=True)
        
    # =============================================================================
    # GERAÇÃO QUERIES COM LIMITE INURLS:(...) ATÉ 4096 CARACTERES
    # =============================================================================
    st.write("")
    st.markdown("### 📝 3. Query de Monitoramento Unificada")
    
    chunks_queries = []
    current_chunk = []
    current_length = 8  # comprimento de prefixo 'inurls:('
    
    for x in ids_unicos:
        formatted_id = f'"{x}"' if '-' in x else x
        addition_length = (4 + len(formatted_id)) if len(current_chunk) > 0 else len(formatted_id) # 4 por causa do " OR "
        
        # Checar se adicionar o elemento ultrapassar 4096 caracteres
        if current_length + addition_length + 1 > 4096:
            if len(current_chunk) > 0:
                chunks_queries.append("inurls:(" + " OR ".join(current_chunk) + ")")
                current_chunk = [formatted_id]
                current_length = 8 + len(formatted_id)
            else:
                chunks_queries.append("inurls:(" + formatted_id + ")")
                current_chunk = []
                current_length = 8
        else:
            current_chunk.append(formatted_id)
            current_length += addition_length
            
    if len(current_chunk) > 0:
        chunks_queries.append("inurls:(" + " OR ".join(current_chunk) + ")")
        
    if len(chunks_queries) > 0:
        if len(chunks_queries) > 1:
            st.warning(f"⚠️ **Atenção:** Como o tamanho total ultrapassaria o limite de 4096 caracteres, geramos de forma automática **{len(chunks_queries)} queries independentes**, respeitando perfeitamente o operador!")
            
        for index, query_text in enumerate(chunks_queries):
            part_matches = len(query_text.replace("inurls:(", "").replace(")", "").split(" OR "))
            st.markdown(f"""
            <div style="background-color:#0A0400;color:#FEFF00;padding:6px 12px;border-top-left-radius:6px;border-top-right-radius:6px;font-size:12px;font-weight:bold;margin-top:10px;">
                🟢 PARTE {index + 1} de {len(chunks_queries)} &middot; {part_matches} IDs &middot; {len(query_text)}/4096 caracteres
            </div>
            """, unsafe_allow_html=True)
            st.code(query_text, language="sql")
            
        # Baixar todas as queries unificadas
        compiled_queries_str = "\n\n".join(chunks_queries)
        st.download_button(
            label="💾 Baixar todas as queries (.txt)",
            data=compiled_queries_str,
            file_name="query_inurls_formatada_completa.txt",
            mime="text/plain"
        )
    else:
        st.info("Nenhum link ativo ou ID válido localizado para montagem do termo booleano. Por favor, verifique se selecionou a coluna certa e se os canais desejados estão ativos.")
        
    # =============================================================================
    # PREVIEW DA TABELA DE EXTRAÇÃO
    # =============================================================================
    st.write("---")
    st.markdown("### 📋 4. Visualização de Links e Identificadores Processados")
    
    if len(df_results_full) > 0:
        # Formatar tabela simplificada para preview
        df_preview = df_results_full[['URL_Original', 'ID_Extraido', 'Canal', 'Resultado']].copy()
        st.dataframe(df_preview, use_container_width=True, hide_index=True)
        
        # Botão para baixar relatório CSV completo
        csv_buffer = io.StringIO()
        df_results_full.to_csv(csv_buffer, index=False, encoding='utf-8-sig', sep=';')
        
        st.download_button(
            label="📥 Baixar Planilha Completa de IDs Extraídos (CSV)",
            data=csv_buffer.getvalue(),
            file_name="cleanquery_relatorio_ids_processados.csv",
            mime="text/csv"
        )
    else:
        st.caption("Sem linhas disponíveis para preview.")
