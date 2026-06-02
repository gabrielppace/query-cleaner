# -*- coding: utf-8 -*-
"""
=============================================================================
CLEANQUERY - STREAMLIT WEB APP
=============================================================================
Este arquivo implementa uma versão interativa em Streamlit da plataforma
CleanQuery para facilitar a distribuição e o uso direto na nuvem (Streamlit Cloud).
=============================================================================
"""

import streamlit as st
import pandas as pd
import re
from urllib.parse import urlparse, parse_qs
import io

# Configuração da página do Streamlit
st.set_page_config(
    page_title="CleanQuery - Extrator de IDs & Query Booleana",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para ficar idêntico ao design sofisticado do React (Slate / Amarelo Burson)
st.markdown("""
<style>
    /* Estilo geral */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Cabeçalhos estilizados */
    .brand-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #0A0400;
        margin-bottom: 0.2rem;
        letter-spacing: -1.5px;
        text-transform: uppercase;
    }
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #555c68;
        margin-bottom: 2rem;
    }
    
    /* Stats */
    .stat-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .stat-val {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0A0400;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    /* Query Box */
    .query-header {
        background-color: #0A0400;
        color: #FEFF00;
        font-weight: 900;
        padding: 0.75rem 1.25rem;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 0.85rem;
        letter-spacing: 1px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .query-box-part {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .query-box-title {
        font-size: 0.8rem;
        font-weight: 850;
        color: #0F172A;
        text-transform: uppercase;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.5rem;
        margin-bottom: 0.75rem;
        display: flex;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# EXTRACTOR CORE LOGIC (Python version of urlParser.ts)
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
# INTERFACE DO USUÁRIO
# =============================================================================

# Cabeçalho da Marca
st.markdown('<div class="brand-title">🔍 CLEANQUERY CLIENT</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">Extrator De IDs de Redes Sociais com Sintetizador de Query Limitada (4096 caracteres)</div>', unsafe_allow_html=True)

# Organização em duas colunas principais
col_config, col_results = st.columns([1, 2], gap="large")

# Estado inicial da aplicação
if 'uploaded_data' not in st.session_state:
    st.session_state['uploaded_data'] = None

with col_config:
    st.subheader("🛠️ Configurações de Entrada")
    
    # Upload do arquivo excel ou csv
    uploaded_file = st.file_uploader(
        "Carregue seu relatório ou planilha (.xlsx, .csv)", 
        type=["xlsx", "csv"],
        help="A planilha deve conter uma coluna com links de redes sociais."
    )
    
    if uploaded_file is not None:
        try:
            # Carregar dados
            if uploaded_file.name.endswith('.csv'):
                df_loaded = pd.read_csv(uploaded_file)
            else:
                df_loaded = pd.read_excel(uploaded_file, engine='openpyxl')
                
            st.session_state['uploaded_data'] = df_loaded
            st.toast("⚡ Arquivo carregado com sucesso!", icon="✅")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            st.session_state['uploaded_data'] = None

    # Tabela com as colunas carregadas se existirem
    if st.session_state['uploaded_data'] is not None:
        df = st.session_state['uploaded_data']
        cols = list(df.columns)
        
        # 1. Identificar coluna de URLs
        url_col_idx = 0
        for i, col in enumerate(cols):
            if col.lower() in ['url', 'link', 'mencion', 'menção', 'endereco', 'endereço']:
                url_col_idx = i
                break
                
        selected_url_col = st.selectbox(
            "Selecione a coluna de URLs:",
            options=cols,
            index=url_col_idx,
            help="Esta coluna contém os links de onde extrairemos os IDs."
        )
        
        # 2. Configurações do Filtro
        st.write("---")
        st.markdown("**📁 Filtrar Registros**")
        
        use_filter = st.checkbox("Habilitar filtro por coluna (ex: Sentimento = Negativo)", value=True)
        
        filter_col_idx = 0
        for i, col in enumerate(cols):
            if col.lower() == 'sentimento':
                filter_col_idx = i
                break
                
        selected_filter_col = st.selectbox(
            "Filtrar por coluna:",
            options=cols,
            index=filter_col_idx,
            disabled=not use_filter
        )
        
        filter_value = st.text_input(
            "Contendo o valor:",
            value="Negativo",
            disabled=not use_filter
        )
        
    else:
        st.info("💡 Carregue uma planilha no botão acima para definir colunas e filtros.")
        selected_url_col = None
        use_filter = False
        selected_filter_col = None
        filter_value = "Negativo"

    # 3. Plataformas Ativas
    st.write("---")
    st.markdown("**🌐 Redes Sociais Ativas**")
    
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

# Lado Direito - Resultados e processamento
with col_results:
    st.subheader("📊 Resultados de Extração & Queries")
    
    if st.session_state['uploaded_data'] is not None:
        df = st.session_state['uploaded_data']
        
        # Filtrar o DataFrame
        if use_filter and selected_filter_col:
            df_filtered = df[df[selected_filter_col].astype(str).str.contains(filter_value, case=False, na=False)].copy()
            total_orig = len(df)
            total_filt = len(df_filtered)
        else:
            df_filtered = df.copy()
            total_orig = len(df)
            total_filt = len(df_filtered)
            
        # Processar
        rows_processed = []
        ids_unicos = []
        
        for idx, row in df_filtered.iterrows():
            url_val = str(row[selected_url_col])
            post_id, platform, is_valid = extrair_id_da_url(url_val, active_platforms)
            
            status = "Sucesso" if is_valid else "Bloqueada"
            
            rows_processed.append({
                'URL_Original': url_val,
                'ID_Extraido': post_id if is_valid else "",
                'Canal': platform.capitalize() if platform != 'others' else 'Outros',
                'Status': status,
                'Valido': is_valid
            })
            
            if is_valid and post_id not in ids_unicos:
                ids_unicos.append(post_id)
                
        df_results_full = pd.DataFrame(rows_processed)
        df_success = df_results_full[df_results_full['Valido'] == True]
        
        # Exibir Cards de Métricas
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{total_filt} / {total_orig}</div>
                <div class="stat-label">linhas após filtro</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{len(df_success)}</div>
                <div class="stat-label">IDs Extraídos</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{len(ids_unicos)}</div>
                <div class="stat-label">IDs Únicos</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        
        # GERAÇÃO DAS QUERIES LIMITADAS A 4096 CARACTERES
        chunks_queries = []
        current_chunk = []
        current_length = 8  # comprimento de 'inurls:('
        
        for x in ids_unicos:
            formatted_id = f'"{x}"' if '-' in x else x
            addition_length = (4 + len(formatted_id)) if len(current_chunk) > 0 else len(formatted_id)
            
            # Checar se ultrapassa 4096 caracteres
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
            
        # Exibição de Query Sintetizada
        st.markdown("### 📝 Query Sintetizada")
        
        if len(chunks_queries) > 0:
            if len(chunks_queries) > 1:
                st.warning(f"⚠️ A query excederia o limite máximo de 4096 caracteres. Geramos **{len(chunks_queries)} queries completas** de forma inteligente!")
                
            for index, query_text in enumerate(chunks_queries):
                matches_count = len(query_text.replace("inurls:(", "").replace(")", "").split(" OR "))
                
                # Exibir Bloco de Query Pronta
                st.markdown(f"""
                <div class="query-box-part">
                    <div class="query-box-title">
                        🟢 Parte {index+1} de {len(chunks_queries)} &middot; {matches_count} IDs &middot; {len(query_text)}/4096 caracteres
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.text_area(f"Copiar Parte {index+1}", value=query_text, height=120, key=f"q_area_{index}")
                
            # Converter queries integradas para download
            complete_queries_raw = "\n\n".join(chunks_queries)
            st.download_button(
                label="💾 Baixar Todas as Queries (.txt)",
                data=complete_queries_raw,
                file_name="cleanquery-todas-queries.txt",
                mime="text/plain"
            )
        else:
            st.info("Nenhum link correspondente ou ID válido encontrado para gerar a query.")
            
        # Preview dos dados extraídos
        st.write("---")
        st.markdown("### 📋 Tabela de Links e IDs Processados")
        
        st.dataframe(
            df_results_full[['URL_Original', 'ID_Extraido', 'Canal', 'Status']],
            use_container_width=True,
            hide_index=True
        )
        
        # Botão para baixar relatório CSV completo
        csv_buffer = io.StringIO()
        df_results_full.to_csv(csv_buffer, index=False, encoding='utf-8-sig', sep=';')
        
        st.download_button(
            label="📥 Baixar Planilha de IDs Extinguidos (CSV)",
            data=csv_buffer.getvalue(),
            file_name="cleanquery_relatorio_ids.csv",
            mime="text/csv"
        )
        
    else:
        # Tela padrão fofa quando não há planilha carregada
        st.write("")
        st.write("")
        st.info("👋 Olá! Por favor, faça upload de uma planilha Excel ou CSV na barra lateral ou na seção de configuração para ver os IDs de mídia social serem extraídos em tempo real e prontos para queries formatadas.")
        
        # Exemplo Simulado
        st.markdown("### 💡 Exemplo de URLs Suportadas")
        exemplo_dados = {
            'URL de Exemplo': [
                'https://www.instagram.com/itatiaiaoficial/p/DVbUsaklPnE/',
                'https://www.facebook.com/radioitatiaia/posts/amazon-conecta-1468483525305135/',
                'https://twitter.com/EInvestidor/status/2036442951404933226',
                'https://youtu.be/dQw4w9WgXcQ'
            ],
            'ID Extraído': ['DVbUsaklPnE', '1468483525305135', '2036442951404933226', 'dQw4w9WgXcQ'],
            'Canal': ['Instagram', 'Facebook', 'Twitter', 'YouTube']
        }
        st.table(pd.DataFrame(exemplo_dados))
