"""
Página para visualizar e gerenciar dispositivos e permissões.
"""
import streamlit as st
import api_client
from utils import get_current_user, set_selected_permission_id, format_datetime, set_selected_device_id

# Configurar página
st.set_page_config(page_title="Meus Dispositivos", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

st.title("📋 Meus Dispositivos")
st.markdown("---")

# Botão para voltar
if st.button("← Voltar ao Painel"):
    st.switch_page("pages/painel.py")

st.markdown("---")

# Carregar dados
try:
    dispositivos = api_client.get_all_dispositivos()
    consentimentos = api_client.get_consentimentos_por_titular(current_user["id"])
except api_client.APIError as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"Erro inesperado: {str(e)}")
    st.stop()

if not dispositivos:
    st.info("Nenhum dispositivo cadastrado no sistema ainda.")
    if st.button("Criar Primeiro Dispositivo"):
        st.switch_page("pages/novo_dispositivo.py")
    st.stop()

# Agrupar consentimentos por dispositivo (excluindo os revogados)
consentimentos_por_dispositivo = {}
for consentimento in consentimentos:
    # Filtrar permissões revogadas - elas não existem para todos os fins
    if consentimento.get("status", "").lower() == "revogado":
        continue
    dispositivo_id = consentimento["dispositivo_id"]
    if dispositivo_id not in consentimentos_por_dispositivo:
        consentimentos_por_dispositivo[dispositivo_id] = []
    consentimentos_por_dispositivo[dispositivo_id].append(consentimento)

# Exibir dispositivos
st.subheader(f"Dispositivos Cadastrados ({len(dispositivos)})")

for dispositivo in dispositivos:
    dispositivo_id = dispositivo["id"]
    dispositivo_nome = dispositivo["nome"]
    dispositivo_localizacao = dispositivo.get("localizacao", "Não informada")
    
    # Contar permissões ativas para este dispositivo
    permissoes_dispositivo = consentimentos_por_dispositivo.get(dispositivo_id, [])
    num_permissoes = len(permissoes_dispositivo)
    
    # Container para cada dispositivo
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 📱 {dispositivo_nome}")
            st.caption(f"📍 Localização: {dispositivo_localizacao}")
            st.caption(f"🔐 Permissões ativas: {num_permissoes}")
        
        with col2:
            if st.button("Ver Detalhes", key=f"btn_{dispositivo_id}", use_container_width=True):
                set_selected_device_id(dispositivo_id)
                st.switch_page("pages/detalhes_dispositivo.py")
        
        st.markdown("---")
