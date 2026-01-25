"""
Aplicação principal do Painel de Controle do Titular.
Ponto de entrada da aplicação Streamlit.
"""
import streamlit as st
from utils import get_current_user

# Configuração da página
st.set_page_config(
    page_title="Painel de Controle do Titular",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Verificar se usuário está logado
current_user = get_current_user()

if not current_user:
    # Redirecionar para login se não estiver logado
    st.switch_page("pages/login.py")
else:
    # Redirecionar para o painel se estiver logado
    st.switch_page("pages/painel.py")
