# -*- coding: utf-8 -*-
"""
=============================================================================
SOCIAL MEDIA QUERY CREATOR - STREAMLIT WEB APP
=============================================================================
Este arquivo implementa a versão interativa em Streamlit da plataforma
Social Media Query Creator para fidedignidade absoluta com o design de marca
revelado no preview do React (Slate, Burson Yellow e Off-White).

Removido abas secundárias a pedido do usuário, focando puramente na 
experiência e refinamento do fluxo interativo principal.
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

# Estilização sob medida com CSS injetado de alto nível para casar exatamente com o design corporativo do React (off-white, slate escuro e amarelo Burson)
st.markdown("""
<style>
    /* Fundo geral moderno off-white e fontes do sistema */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;550;700&display=swap');
    
    .stApp {
        background-color: #F8FAFC !important;
        color: #0A0400 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Configuração do Header com o mesmo estilo do React, utilizando a premissa de luxo Burson */
    .b-header {
        background-color: #0A0400;
        color: #FFFFF1;
        padding: 1.5rem 2rem;
        border-bottom: 4px solid #FEFF00;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .b-title-group {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .b-logo {
        background-color: #FEFF00;
        color: #0A0400;
        font-size: 24px;
        font-weight: 900;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        border: 2px solid #FEFF00;
        font-family: 'Inter', sans-serif;
    }
    
    .b-title-texts h1 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        color: #FFFFF1 !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        line-height: 1.2;
    }
    
    .b-title-texts p {
        margin: 4px 0 0 0 !important;
        font-size: 0.75rem !important;
        color: #94a3b8 !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .b-badge {
        background-color: #FEFF00;
        color: #0A0400;
        font-size: 9px;
        font-weight: 950;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-left: 8px;
        display: inline-block;
        vertical-align: middle;
    }
    
    /* Configuração de Toggles e Filtros */
    .section-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01);
    }
    
    .section-title {
        font-size: 0.75rem;
        font-weight: 800;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.5rem;
    }
    
    /* Cartões de Métricas elegantes com borda amarela Burson */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card-styled {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0A0400;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        transition: all 0.2s ease;
    }
    
    .metric-card-styled:hover {
        transform: translateY(-1px);
        border-left: 4px solid #FEFF00;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .metric-val-num {
        font-size: 1.6rem;
        font-weight: 900;
        color: #0A0400;
        line-height: 1;
    }
    
    .metric-lbl-text {
        font-size: 0.65rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.4rem;
    }
    
    /* Customização dos botões do Streamlit */
    div.stButton > button {
        background-color: #0A0400 !important;
        color: #FEFF00 !important;
        font-weight: 800 !important;
        border: 1px solid #0A0400 !important;
        border-radius: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button:hover {
        background-color: #222222 !important;
        border-color: #222222 !important;
        color: #FEFF00 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }

    /* Info Alert no topo */
    .top-info {
        background-color: rgba(254, 255, 0, 0.08);
        border: 1px solid rgba(10, 4, 0, 0.12);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# REPLICAÇÃO DOS DADOS DO RELATÓRIO DO /src/data.ts
# =============================================================================
SAMPLE_ROW_DATA = [
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
# EXTRATOR CORE LOGIC (Python matching /src/utils/urlParser.ts exactly)
# =============================================================================
def extrair_id_da_url(url: str, active_platforms: dict) -> tuple:
    if not isinstance(url, str) or not url.strip():
        return "", "others", False

    trimmed = url.strip()

    # 1. Twitter / X
    if ("twitter.com" in trimmed or "x.com" in trimmed) and active_platforms.get('twitter', True):
        twitter_regex = r'(?:twitter\.com|x\.com)/[^/]+/status/(\d+)'
        match = re.search(twitter_regex, trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'twitter', True
            
        fallback_match = re.search(r'/(\d+)/?(?:\?|$)', trimmed)
        if fallback_match:
            return fallback_match.group(1), 'twitter', True

    # 2. Facebook
    elif "facebook.com" in trimmed and active_platforms.get('facebook', True):
        normalized_url = trimmed.rstrip('/')
        match_end_num = re.search(r'/(\d{6,25})(?:\?|#|$)', normalized_url)
        if match_end_num:
            return match_end_num.group(1), 'facebook', True

        posts_regex = r'/posts/(\d+)'
        match = re.search(posts_regex, trimmed, re.IGNORECASE)
        if match:
            return match.group(1), 'facebook', True

        groups_regex = r'/permalink/(\d+)'
        match_perm = re.search(groups_regex, trimmed, re.IGNORECASE)
        if match_perm:
            return match_perm.group(1), 'facebook', True

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

        match_gen = re.search(r'/posts/([^/?]+)', trimmed, re.IGNORECASE)
        if match_gen:
            id_only = match_gen.group(1).split('?')[0]
            has_word_hyphens = id_only.count('-') > 2
            is_plain_word = re.match(r'^[A-Za-z_-]+$', id_only) and len(id_only) > 5
            if not has_word_hyphens and not is_plain_word:
                return id_only, 'facebook', True

    # 3. Instagram
    elif "instagram.com" in trimmed and active_platforms.get('instagram', True):
        match_direct = re.search(r'instagram\.com/(?:p|reel|tv)/([^/?]+)', trimmed, re.IGNORECASE)
        if match_direct:
            return match_direct.group(1), 'instagram', True
            
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

    # Robust Fallback genérico para sequências numéricas (idêntico ao original do React)
    try:
        end_numeric_match = re.search(r'/(\d{6,25})/?(?:\?|#|$)', trimmed)
        if end_numeric_match:
            return end_numeric_match.group(1), 'others', True

        body_numeric_match = re.search(r'(?:^|/|\D)(\d{8,25})(?:\D|$)', trimmed)
        if body_numeric_match:
            return body_numeric_match.group(1), 'others', True

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
# CONSTRUÇÃO DO HEADER IDENTIDADE CORPORATIVA BURSON
# =============================================================================
st.markdown("""
<div class="b-header">
    <div class="b-title-group">
        <div class="b-logo">B</div>
        <div class="b-title-texts">
            <h1>Social Media Query Creator <span class="b-badge">PRO</span></h1>
            <p>Integração de Relatórios & Purificador de Identificadores de Mídia Social</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# INTERFACE INTERATIVA PRINCIPAL (SEM ABAS COADJUVANTES)
# =============================================================================

# Top Info Alert igual ao React
st.markdown("""
<div class="top-info">
    <div style="font-size: 0.725rem; font-weight: 800; color: #0A0400; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
        Como funciona este fluxo interativo?
    </div>
    <div style="font-size: 0.775rem; color: #334155; line-height: 1.4;">
        Este simulador reproduz o comportamento exato que o seu script realiza: ele pega as URLs,
        aplica as condições de filtragem definidas, descarta links inválidos trazendo apenas os identificadores (IDs puros),
        e agrupa-os na query booleana usando o operador <code>inurls:(...)</code> respeitando o limite máximo estrutural de 4096 caracteres.
    </div>
</div>
""", unsafe_allow_html=True)

# Grid de Layout Principal (Painel Lateral de configs e Resultados)
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    # Configuração de Entrada de Dados
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Origem dos Dados</div>', unsafe_allow_html=True)
    
    input_type = st.radio(
        "Origem das URLs:",
        [
            "Colar links diretamente (Mais rápido)", 
            "Carregar planilha de relatório (.xlsx, .csv)", 
            "Carregar dados de simulação Burson"
        ],
        index=0
    )
    
    raw_text_links = ""
    uploaded_df = None
    
    if input_type == "Colar links diretamente (Mais rápido)":
        raw_text_links = st.text_area(
            "Cole seus links (um por linha):",
            placeholder="https://www.instagram.com/p/C7X3x1uuW8z/\nhttps://twitter.com/EInvestidor/status/2036442951404933226\nhttps://www.facebook.com/radioitatiaia/posts/1468483525305135",
            height=150
        ).strip()
        
    elif input_type == "Carregar planilha de relatório (.xlsx, .csv)":
        uploaded_file = st.file_uploader(
            "Selecione uma planilha de menções:",
            type=["xlsx", "xls", "csv"]
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    uploaded_df = pd.read_csv(uploaded_file)
                else:
                    uploaded_df = pd.read_excel(uploaded_file, engine='openpyxl')
                st.success("Tabela carregada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao analisar arquivo: {e}")
        else:
            st.info("Aguardando upload de planilha...")
            
    else:
        # Usar dados simulados
        uploaded_df = pd.DataFrame(SAMPLE_ROW_DATA)
        st.info("Demonstração ativa com as 12 menções padrão de amostra.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Seleção de Colunas e Filtros
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Mapeamento & Condições</div>', unsafe_allow_html=True)
    
    sel_url_col = "URL"
    sel_filter_col = ""
    sel_filter_val = ""
    
    # Se temos uma tabela de entrada (seja carregada ou simulação)
    if uploaded_df is not None:
        available_cols = list(uploaded_df.columns)
        
        # Tentar autodetectar URL
        auto_idx = 0
        for i, col in enumerate(available_cols):
            if col.lower() in ['url', 'link', 'mencion', 'menção', 'endereco', 'endereço']:
                auto_idx = i
                break
                
        sel_url_col = st.selectbox(
            "Coluna de URLs:",
            options=available_cols,
            index=auto_idx
        )
        
        enable_conditions = st.checkbox("Aplicar filtragem interna por valor", value=False)
        if enable_conditions:
            # Tentar autodetectar sentimento
            filt_idx = 0
            for i, col in enumerate(available_cols):
                if col.lower() in ['sentimento', 'sentiment', 'tags', 'mídia', 'canal']:
                    filt_idx = i
                    break
                    
            sel_filter_col = st.selectbox(
                "Coluna para Filtrar:",
                options=available_cols,
                index=filt_idx
            )
            sel_filter_val = st.text_input(
                "Filtrar por esse valor (contendo):",
                value="Negativo"
            )
    else:
        st.caption("Mapeamento dinâmico indisponível em colagem manual (usa campo único de texto).")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtros e Canais Ativos
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Canais Ativos</div>', unsafe_allow_html=True)
    
    active_tw = st.toggle("Twitter / X", value=True)
    active_fb = st.toggle("Facebook", value=True)
    active_ig = st.toggle("Instagram", value=True)
    active_tk = st.toggle("TikTok", value=True)
    active_yt = st.toggle("YouTube", value=True)
    active_lk = st.toggle("LinkedIn", value=True)
    
    active_platforms = {
        'twitter': active_tw,
        'facebook': active_fb,
        'instagram': active_ig,
        'tiktok': active_tk,
        'youtube': active_yt,
        'linkedin': active_lk,
        'others': True
    }
    
    st.write("---")
    preemptive_remove_linkedin = st.checkbox(
        "Ignorar URLs do LinkedIn antes do filtro", 
        value=True,
        help="Descarta preventivamente links de linkedin.com para aliviar tamanho de query booleana."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
with col_right:
    # Preencher DataFrame inicial de trabalho
    df_work = pd.DataFrame()
    
    if input_type == "Colar links diretamente (Mais rápido)":
        if raw_text_links:
            lines = [l.strip() for l in raw_text_links.split('\n') if l.strip()]
            df_work = pd.DataFrame({'URL': lines})
            sel_url_col = 'URL'
    else:
        if uploaded_df is not None:
            df_work = uploaded_df.copy()
            
    # Começar o processamento
    if not df_work.empty:
        total_linhas_iniciais = len(df_work)
        
        # Aplicar filtro de LinkedIn preemptivo
        if preemptive_remove_linkedin and sel_url_col in df_work.columns:
            df_work = df_work[~df_work[sel_url_col].astype(str).str.lower().str.contains('linkedin.com', na=False)]
            
        # Aplicar filtro de valor se habilitado
        if sel_filter_col and sel_filter_val:
            df_work = df_work[df_work[sel_filter_col].astype(str).str.contains(sel_filter_val, case=False, na=False)]
            
        total_linhas_filtradas = len(df_work)
        
        # Rodar extrator de IDs
        rows_processed = []
        ids_unicos = []
        
        for idx, row in df_work.iterrows():
            url_val = str(row.get(sel_url_col, "")).strip()
            if not url_val or url_val.lower() == 'nan':
                continue
                
            post_id, platform, is_valid = extrair_id_da_url(url_val, active_platforms)
            
            status_txt = "Sucesso" if is_valid else "Não identificado/Descartado"
            
            rows_processed.append({
                'URL_Original': url_val,
                'ID_Extraido': post_id if is_valid else "",
                'Canal': platform,
                'Resultado': status_txt,
                'Valido': is_valid
            })
            
            if is_valid and post_id not in ids_unicos:
                ids_unicos.append(post_id)
                
        df_results = pd.DataFrame(rows_processed)
        total_ids_extraidos = len(df_results[df_results['Valido'] == True]) if not df_results.empty else 0
        total_ids_unicos = len(ids_unicos)
        
        # Exibir Métricas idênticas à UI do React
        st.markdown(f"""
        <div class="metrics-container">
            <div class="metric-card-styled">
                <div class="metric-val-num">{total_linhas_iniciais}</div>
                <div class="metric-lbl-text">LINHAS TOTAIS</div>
            </div>
            <div class="metric-card-styled">
                <div class="metric-val-num">{total_linhas_filtradas}</div>
                <div class="metric-lbl-text">FILTRADAS/ATIVAS</div>
            </div>
            <div class="metric-card-styled">
                <div class="metric-val-num">{total_ids_extraidos}</div>
                <div class="metric-lbl-text">IDS EXTRAÍDOS</div>
            </div>
            <div class="metric-card-styled">
                <div class="metric-val-num">{total_ids_unicos}</div>
                <div class="metric-lbl-text">IDS ÚNICOS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Geração das Queries Limitadas a 4096 caracteres
        st.markdown("### Resultado da Query Sintetizada")
        
        chunks_queries = []
        current_chunk = []
        current_length = 8  # comprimento de prefixo 'inurls:('
        
        for x in ids_unicos:
            formatted_id = f'"{x}"' if '-' in x else x
            addition_length = (4 + len(formatted_id)) if len(current_chunk) > 0 else len(formatted_id)
            
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
            
        if chunks_queries:
            if len(chunks_queries) > 1:
                st.warning(f"Aviso: Visto que a quantidade excede o limite máximo de caracteres no monitoramento, geramos {len(chunks_queries)} blocos de queries autocontidas automaticamente.")
                
            for idx, query in enumerate(chunks_queries):
                sub_ids_count = len(query.replace("inurls:(", "").replace(")", "").split(" OR "))
                
                st.markdown(f"""
                <div style="background-color: #0A0400; color: #FEFF00; padding: 6px 12px; border-radius: 6px 6px 0 0; font-size: 11px; font-weight: 900; margin-top: 15px; text-transform: uppercase;">
                    Query Parte {idx+1} de {len(chunks_queries)} &middot; {sub_ids_count} IDs &middot; {len(query)}/4096 caracteres
                </div>
                """, unsafe_allow_html=True)
                st.code(query, language="sql")
                
            # Download das queries formatadas em arquivo TXT único
            txt_compilation = "\n\n".join(chunks_queries)
            st.download_button(
                label="BAIXAR BLOCOS DE QUERY (TXT)",
                data=txt_compilation,
                file_name="burson_queries_geradas.txt",
                key="btn_download_txt"
            )
        else:
            st.info("Nenhum ID social identificado para agrupar na query booleana.")
            
        # Tabela de Preview idêntica à do React
        st.write("---")
        st.markdown("### Preview dos Links e Identificadores")
        
        if not df_results.empty:
            df_rendered = df_results.copy()
            df_rendered['Canal'] = df_rendered['Canal'].apply(lambda x: x.upper() if isinstance(x, str) else x)
            st.dataframe(
                df_rendered[['URL_Original', 'ID_Extraido', 'Canal', 'Resultado']], 
                use_container_width=True,
                hide_index=True
            )
            
            # Download de Planilha de IDs Isolados integrada
            csv_buffer = io.StringIO()
            df_rendered.to_csv(csv_buffer, index=False, encoding='utf-8-sig', sep=';')
            st.download_button(
                label="BAIXAR PLANILHA COMPLETA (CSV)",
                data=csv_buffer.getvalue(),
                file_name="cleanquery_relatorio_ids_isolados.csv",
                mime="text/csv",
                key="btn_download_csv"
            )
    else:
        st.info("Comece inserindo URLs válidas ou carregando planilhas na barra lateral esquerda para iniciar o monitoramento em tempo real.")
        
        # Exibir amostra visual se estiver vazio
        st.markdown("#### Exemplo de Links Processados pelo Sistema:")
        ex_data = {
            'Link do Post': [
                'https://twitter.com/GabrielPace/status/1789234567891234567',
                'https://www.instagram.com/p/DVbUsaklPnE/',
                'https://www.facebook.com/radioitatiaia/posts/1468483525305135'
            ],
            'ID Extraído': ['1789234567891234567', 'DVbUsaklPnE', '1468483525305135'],
            'Plataforma': ['Twitter / X', 'Instagram', 'Facebook']
        }
        st.table(pd.DataFrame(ex_data))
