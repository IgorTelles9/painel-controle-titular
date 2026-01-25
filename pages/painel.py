"""
Página principal do painel de controle.
"""
import streamlit as st
from utils import get_current_user

# Configurar página
st.set_page_config(page_title="Painel de Controle", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

# Header
st.title("🏠 Painel de Controle")
st.markdown(f"**Bem-vindo, {current_user['nome']}!**")
st.markdown("---")

# Botões principais
st.subheader("Escolha uma opção:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📱 Novo Dispositivo")
    st.markdown("Registre um novo dispositivo IoT no sistema.")
    if st.button("Novo Dispositivo", use_container_width=True, type="primary"):
        st.switch_page("pages/novo_dispositivo.py")

with col2:
    st.markdown("### 🔐 Nova Permissão")
    st.markdown("Configure permissões de consentimento para um dispositivo.")
    if st.button("Nova Permissão", use_container_width=True, type="primary"):
        # Limpar pending_device ao acessar pelo botão do painel
        from utils import clear_pending_device, clear_edit_permission_data
        clear_pending_device()
        clear_edit_permission_data()
        st.switch_page("pages/nova_permissao.py")

with col3:
    st.markdown("### 📋 Meus Dispositivos")
    st.markdown("Visualize e gerencie seus dispositivos e permissões.")
    if st.button("Meus Dispositivos", use_container_width=True, type="primary"):
        st.switch_page("pages/meus_dispositivos.py")

st.markdown("---")

# Informações do usuário
with st.expander("ℹ️ Informações da Conta"):
    st.write(f"**Nome:** {current_user['nome']}")
    st.write(f"**Email:** {current_user['email']}")
    st.write(f"**ID:** {current_user['id']}")
