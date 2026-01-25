"""
Página para criar um novo dispositivo.
"""
import streamlit as st
import api_client
from utils import get_current_user, set_pending_device

# Configurar página
st.set_page_config(page_title="Novo Dispositivo", page_icon="📱", layout="centered", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

# Limpar estado ao entrar na página (resetar formulário)
# Usar uma chave única para rastrear se estamos em um fluxo ativo
if "novo_dispositivo_active" not in st.session_state:
    # Primeira vez na página ou voltando de outra página - limpar estado
    if "dispositivo_criado" in st.session_state:
        del st.session_state["dispositivo_criado"]
    if "pending_device_id" in st.session_state:
        del st.session_state["pending_device_id"]
    st.session_state["novo_dispositivo_active"] = True

st.title("📱 Novo Dispositivo")
st.markdown("---")

# Botão para voltar
if st.button("← Voltar ao Painel"):
    # Limpar estado ao sair da página
    if "dispositivo_criado" in st.session_state:
        del st.session_state["dispositivo_criado"]
    if "pending_device_id" in st.session_state:
        del st.session_state["pending_device_id"]
    if "novo_dispositivo_active" in st.session_state:
        del st.session_state["novo_dispositivo_active"]
    st.switch_page("pages/painel.py")

st.markdown("---")

# Verificar se há um dispositivo recém-criado aguardando ação
if "dispositivo_criado" in st.session_state:
    dispositivo_info = st.session_state["dispositivo_criado"]
    st.success(f"Dispositivo '{dispositivo_info['nome']}' criado com sucesso! 🎉")
    
    st.markdown("---")
    st.subheader("Próximos Passos")
    st.info("Agora você pode configurar as permissões de consentimento para este dispositivo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Configurar Permissões do Dispositivo", use_container_width=True, type="primary"):
            # Manter o pending_device_id para a próxima página
            # Limpar apenas o dispositivo_criado pois já foi processado
            if "dispositivo_criado" in st.session_state:
                del st.session_state["dispositivo_criado"]
            # Limpar flag para resetar quando voltar
            if "novo_dispositivo_active" in st.session_state:
                del st.session_state["novo_dispositivo_active"]
            st.switch_page("pages/nova_permissao.py")
    
    with col2:
        if st.button("⏭️ Agora Não", use_container_width=True):
            st.warning(f"⚠️ Nenhum dado coletado pelo dispositivo '{dispositivo_info['nome']}' será transmitido. Acesse o menu de permissões para alterar isso.")
            # Limpar estado após mostrar aviso
            if "dispositivo_criado" in st.session_state:
                del st.session_state["dispositivo_criado"]
            if "pending_device_id" in st.session_state:
                del st.session_state["pending_device_id"]
            if "novo_dispositivo_active" in st.session_state:
                del st.session_state["novo_dispositivo_active"]
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Ou criar outro dispositivo:")

# Formulário de criação
with st.form("novo_dispositivo_form"):
    st.subheader("Informações do Dispositivo")
    
    nome = st.text_input("Nome do Dispositivo *", placeholder="Ex: Sensor de Temperatura Sala 1")
    localizacao = st.text_input("Localização (opcional)", placeholder="Ex: Sala de Estar, Andar 1")
    
    st.caption("* Campos obrigatórios")
    
    submitted = st.form_submit_button("Criar Dispositivo", use_container_width=True, type="primary")
    
    if submitted:
        if not nome:
            st.error("Por favor, preencha o nome do dispositivo.")
        else:
            try:
                # Criar dispositivo
                novo_dispositivo = api_client.create_dispositivo(
                    nome=nome,
                    localizacao=localizacao if localizacao else None
                )
                
                # Armazenar dispositivo pendente na sessão
                set_pending_device(novo_dispositivo["id"])
                
                # Armazenar informações do dispositivo criado para exibir os botões
                st.session_state["dispositivo_criado"] = {
                    "id": novo_dispositivo["id"],
                    "nome": novo_dispositivo["nome"]
                }
                
                # Recarregar a página para mostrar os botões
                st.rerun()
                
            except api_client.APIError as e:
                st.error(f"Erro ao criar dispositivo: {str(e)}")
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")
