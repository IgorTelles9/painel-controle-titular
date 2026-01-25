"""
Página para visualizar detalhes de um dispositivo e suas permissões.
"""
import streamlit as st
import api_client
from utils import (
    get_current_user,
    set_selected_permission_id,
    format_datetime,
    get_selected_device_id,
    set_selected_device_id
)

# Configurar página
st.set_page_config(page_title="Detalhes do Dispositivo", page_icon="📱", layout="wide", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

# Obter ID do dispositivo da sessão
dispositivo_id = get_selected_device_id()
if not dispositivo_id:
    st.error("Nenhum dispositivo selecionado.")
    st.info("Volte para a lista de dispositivos e selecione um dispositivo.")
    if st.button("← Voltar aos Dispositivos"):
        st.switch_page("pages/meus_dispositivos.py")
    st.stop()

# Carregar dados
try:
    dispositivo = api_client.get_dispositivo(dispositivo_id)
    consentimentos = api_client.get_consentimentos_por_titular(current_user["id"])
    
    # Filtrar consentimentos apenas deste dispositivo e excluir os revogados
    consentimentos_dispositivo = [
        c for c in consentimentos 
        if c["dispositivo_id"] == dispositivo_id 
        and c.get("status", "").lower() != "revogado"
    ]
    
    # Carregar dados adicionais para exibição
    finalidades = {f["id"]: f for f in api_client.get_all_finalidades()}
    tipos_dados = {t["id"]: t for t in api_client.get_all_tipos_dados()}
    opcoes_tratamento = {o["id"]: o for o in api_client.get_all_opcoes_tratamento()}
    
except api_client.APIError as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"Erro inesperado: {str(e)}")
    st.stop()

st.title("📱 Detalhes do Dispositivo")
st.markdown("---")

# Botão para voltar
if st.button("← Voltar aos Dispositivos"):
    if "selected_device_id" in st.session_state:
        del st.session_state["selected_device_id"]
    st.switch_page("pages/meus_dispositivos.py")

st.markdown("---")

# Informações do dispositivo
st.subheader("📋 Informações do Dispositivo")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.write(f"**ID:** {dispositivo.get('id', 'N/A')}")
    st.write(f"**Nome:** {dispositivo.get('nome', 'N/A')}")
with col_info2:
    st.write(f"**Localização:** {dispositivo.get('localizacao', 'Não informada')}")
    if dispositivo.get("created_at"):
        st.write(f"**Criado em:** {format_datetime(dispositivo['created_at'])}")

st.markdown("---")

# Permissões
st.subheader("🔐 Permissões de Consentimento")

num_permissoes = len(consentimentos_dispositivo)

if num_permissoes == 0:
    st.info("Este dispositivo não possui permissões configuradas ainda.")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Criar Primeira Permissão", use_container_width=True, type="primary"):
            from utils import set_pending_device, clear_edit_permission_data
            set_pending_device(dispositivo_id)
            clear_edit_permission_data()
            st.switch_page("pages/nova_permissao.py")
    with col2:
        if st.button("← Voltar aos Dispositivos", use_container_width=True):
            if "selected_device_id" in st.session_state:
                del st.session_state["selected_device_id"]
            st.switch_page("pages/meus_dispositivos.py")
else:
    st.markdown(f"**Total de permissões ativas:** {num_permissoes}")
    st.markdown("")
    
    for idx, consentimento in enumerate(consentimentos_dispositivo):
        # Buscar informações relacionadas
        opcao_id = consentimento.get("opcao_tratamento_id")
        tipo_dado_id = consentimento.get("tipo_de_dado_id")
        
        opcao_info = opcoes_tratamento.get(opcao_id, {})
        tipo_dado_info = tipos_dados.get(tipo_dado_id, {})
        
        opcao_titulo = opcao_info.get("titulo", "N/A")
        tipo_dado_nome = tipo_dado_info.get("nome", "N/A")
        data_registro = consentimento.get("data_registro", "")
        
        if data_registro:
            data_formatada = format_datetime(data_registro)
        else:
            data_formatada = "N/A"
        
        # Texto do botão
        button_text = f"{opcao_titulo} - {tipo_dado_nome} - {data_formatada}"
        
        # Botão para ver detalhes da permissão
        if st.button(
            button_text,
            key=f"perm_{consentimento['id']}",
            use_container_width=True
        ):
            set_selected_permission_id(consentimento["id"])
            st.switch_page("pages/detalhes_permissao.py")
