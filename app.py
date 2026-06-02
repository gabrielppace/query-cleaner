# -*- coding: utf-8 -*-
"""
=============================================================================
SOCIAL MEDIA QUERY CREATOR - STREAMLIT WEB APP
=============================================================================
Este arquivo implementa a versão interativa em Streamlit da plataforma
Social Media Query Creator para fidedignidade absoluta com o design de marca
revelado no preview do React (Slate, Burson Yellow e Off-White).

Removido abas secundárias, dados de simulação e ajustado o sistema de 
caixas (section-box) retirando tags HTML fragmentadas que geravam caixas vazias.
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

# Estilização sob medida com CSS injetado de alto nível para casar exatamente com o design corporativo (off-white, slate escuro e amarelo Burson)
st.markdown("""
<style>
    /* Fundo geral moderno off-white e fontes do sistema */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;550;700&display=swap');
    
    .stApp {
        background-color: #F8FAFC !important;
        color: #0A0400 !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Configuração do Header com a premissa de luxo Burson */
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
    
    /* Títulos de Seção Internos estilizados no padrão Burson */
    .b-section-header {
        font-size: 0.8rem !important;
        font-weight: 800 !important;
        color: #0A0400 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-top: 0px !important;
        margin-bottom: 12px !important;
        border-bottom: 2px solid #FEFF00 !important;
        padding-bottom: 4px !important;
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
        width: 100% !important;
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

    /* Estilização sutil para os widgets nativos de container do streamlit */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01) !important;
    }
</style>
""", unsafe_allow_html=True)


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
# INTERFACE INTERATIVA PRINCIPAL
# =============================================================================

# Top Info Alert igual ao React
st.markdown("""
<div class="top-info">
    <div style="font-size: 0.725rem; font-weight: 800; color: #0A0400; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
        Como funciona este fluxo interativo?
    </div>
    <div style="font-size: 0.775rem; color: #334155; line-height: 1.4;">
        Este simulador processa as URLs fornecidas, aplica as condições de filtragem selecionadas, 
        extrai exclusivamente os IDs de canais ativos, descarta links inválidos e gera blocos de query 
        higienizados no formato <code>inurls:(...)</code> respeitando o limite do monitoramento de 4096 caracteres.
    </div>
</div>
""", unsafe_allow_html=True)

# Grid de Layout Principal (Painel Lateral de configs e Resultados)
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    # 1. Container de Origem dos Dados
    with st.container(border=True):
        st.markdown('<div class="b-section-header">Origem dos Dados</div>', unsafe_allow_html=True)
        
        input_type = st.radio(
            "Origem das URLs:",
            [
                "Colar links diretamente (Mais rápido)", 
                "Carregar planilha de relatório (.xlsx, .csv)"
            ],
            index=0
        )
        
        raw_text_links = ""
        uploaded_df = None
        
        if input_type == "Colar links diretamente (Mais rápido)":
            raw_text_links = st.text_area(
                "Cole seus links (um por linha):",
                placeholder="https://www.instagram.com/p/C7X3x1uuW8z/\nhttps://twitter.com/EInvestidor/status/2036442951404933226\nhttps://www.facebook.com/radioitatiaia/posts/1468483525305135",
                height=180
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

    # 2. Container de Mapeamento & Condições
    with st.container(border=True):
        st.markdown('<div class="b-section-header">Mapeamento & Condições</div>', unsafe_allow_html=True)
        
        sel_url_col = "URL"
        sel_filter_col = ""
        sel_filter_val = ""
        
        # Se temos uma tabela de entrada
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
                # Tentar autodetectar sentimento/tags
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
            st.caption("Filtros por coluna disponíveis no upload de planilha.")

    # 3. Container de Canais Ativos
    with st.container(border=True):
        st.markdown('<div class="b-section-header">Canais e Exclusões</div>', unsafe_allow_html=True)
        
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
        
        preemptive_remove_linkedin = st.checkbox(
            "Ignorar links LinkedIn antes do filtro", 
            value=True,
            help="Descarte preventivo de domínios linkedin.com para reduzir tamanho de queries booleanas."
        )

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
        
        # Exibir Métricas
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
        current_length = 8  # comprimento de 'inurls:('
        
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
            st.info("Nenhum ID social válido identificado com as regras selecionadas.")
            
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
        st.info("Comece inserindo as URLs ou carregando planilhas na barra lateral para ver o monitoramento em tempo real.")
        
        # Exibir amostra do layout de resultado se estiver vazio
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
