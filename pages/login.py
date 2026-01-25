"""
Página de login e registro de usuários.
"""
import streamlit as st
import api_client
from utils import get_current_user, set_current_user, clear_session

# Configurar página
st.set_page_config(page_title="Login - Painel de Controle", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")

# Verificar se já está logado
if get_current_user():
    st.switch_page("pages/painel.py")

st.title("🔐 Login")
st.markdown("---")

# Inicializar estado do formulário
if "show_register" not in st.session_state:
    st.session_state.show_register = False

# Toggle entre login e registro
col1, col2 = st.columns(2)
with col1:
    if st.button("Login", use_container_width=True, type="primary" if not st.session_state.show_register else "secondary"):
        st.session_state.show_register = False
        st.rerun()

with col2:
    if st.button("Registrar", use_container_width=True, type="primary" if st.session_state.show_register else "secondary"):
        st.session_state.show_register = True
        st.rerun()

st.markdown("---")

if st.session_state.show_register:
    # Formulário de Registro
    st.subheader("Criar Nova Conta")
    
    with st.form("register_form"):
        nome = st.text_input("Nome completo", placeholder="Digite seu nome")
        email = st.text_input("Email", placeholder="seu@email.com")
        
        submitted = st.form_submit_button("Registrar", use_container_width=True, type="primary")
        
        if submitted:
            if not nome or not email:
                st.error("Por favor, preencha todos os campos.")
            else:
                try:
                    # Verificar se o email já existe
                    titular_existente = api_client.get_titular_by_email(email)
                    
                    if titular_existente:
                        st.error("Este email já está cadastrado. Faça login ou use outro email.")
                    else:
                        # Criar novo titular
                        novo_titular = api_client.create_titular(nome=nome, email=email)
                        set_current_user(novo_titular)
                        st.success(f"Conta criada com sucesso! Bem-vindo, {nome}!")
                        st.balloons()
                        st.rerun()
                except api_client.APIError as e:
                    st.error(f"Erro ao criar conta: {str(e)}")
                except Exception as e:
                    st.error(f"Erro inesperado: {str(e)}")

else:
    # Formulário de Login
    st.subheader("Entrar na sua conta")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        
        submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
        
        if submitted:
            if not email:
                st.error("Por favor, digite seu email.")
            else:
                try:
                    titular = api_client.get_titular_by_email(email)
                    
                    if titular:
                        set_current_user(titular)
                        st.success(f"Bem-vindo de volta, {titular['nome']}!")
                        st.rerun()
                    else:
                        st.session_state.login_email_not_found = email
                        st.rerun()
                except api_client.APIError as e:
                    st.error(f"Erro ao fazer login: {str(e)}")
                except Exception as e:
                    st.error(f"Erro inesperado: {str(e)}")

# Mostrar aviso se email não foi encontrado (fora do form)
if "login_email_not_found" in st.session_state and not st.session_state.show_register:
    st.warning(f"Email '{st.session_state.login_email_not_found}' não encontrado. Deseja criar uma nova conta?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim, criar conta", key="create_from_login", use_container_width=True):
            st.session_state.show_register = True
            if "login_email_not_found" in st.session_state:
                del st.session_state.login_email_not_found
            st.rerun()
    with col2:
        if st.button("Não, tentar outro email", key="try_another_email", use_container_width=True):
            if "login_email_not_found" in st.session_state:
                del st.session_state.login_email_not_found
            st.rerun()
