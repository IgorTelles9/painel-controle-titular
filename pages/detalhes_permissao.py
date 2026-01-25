"""
Página para visualizar detalhes de uma permissão e realizar ações (alterar/revogar).
"""
import streamlit as st
import api_client
from utils import (
    get_current_user,
    get_selected_permission_id,
    set_edit_permission_data,
    format_datetime,
    set_selected_device_id
)

# Configurar página
st.set_page_config(page_title="Detalhes da Permissão", page_icon="🔍", layout="centered", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

st.title("🔍 Detalhes da Permissão")
st.markdown("---")

# Botão para voltar
if st.button("← Voltar aos Dispositivos"):
    st.switch_page("pages/meus_dispositivos.py")

st.markdown("---")

# Obter ID da permissão
permission_id = get_selected_permission_id()
if not permission_id:
    st.error("Nenhuma permissão selecionada.")
    st.info("Volte para a lista de dispositivos e selecione uma permissão.")
    st.stop()

# Carregar dados
try:
    # Buscar todos os consentimentos do usuário para encontrar o selecionado
    consentimentos = api_client.get_consentimentos_por_titular(current_user["id"])
    # Filtrar permissões revogadas - elas não existem para todos os fins
    consentimentos_ativos = [c for c in consentimentos if c.get("status", "").lower() != "revogado"]
    consentimento = next((c for c in consentimentos_ativos if c["id"] == permission_id), None)
    
    if not consentimento:
        st.error("Permissão não encontrada ou você não tem permissão para visualizá-la.")
        st.stop()
    
    # Carregar dados relacionados
    dispositivo = api_client.get_dispositivo(consentimento["dispositivo_id"])
    
    # Carregar listas para buscar informações relacionadas
    finalidades = {f["id"]: f for f in api_client.get_all_finalidades()}
    tipos_dados = {t["id"]: t for t in api_client.get_all_tipos_dados()}
    opcoes_tratamento = {o["id"]: o for o in api_client.get_all_opcoes_tratamento()}
    
    # Obter informações relacionadas
    finalidade = finalidades.get(consentimento["finalidade_id"], {})
    tipo_dado = tipos_dados.get(consentimento["tipo_de_dado_id"], {})
    opcao_tratamento = opcoes_tratamento.get(consentimento["opcao_tratamento_id"], {})
    
except api_client.APIError as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"Erro inesperado: {str(e)}")
    st.stop()

# Exibir informações
st.subheader("📋 Informações Gerais")

col1, col2 = st.columns(2)
with col1:
    st.write(f"**ID da Permissão:** {consentimento['id']}")
    st.write(f"**Status:** {consentimento.get('status', 'N/A')}")
    if consentimento.get("data_registro"):
        st.write(f"**Data de Registro:** {format_datetime(consentimento['data_registro'])}")
with col2:
    if consentimento.get("data_revogacao"):
        st.write(f"**Data de Revogação:** {format_datetime(consentimento['data_revogacao'])}")
    if consentimento.get("data_expiracao"):
        st.write(f"**Data de Expiração:** {format_datetime(consentimento['data_expiracao'])}")

st.markdown("---")

st.subheader("📱 Dispositivo")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Nome:** {dispositivo.get('nome', 'N/A')}")
    st.write(f"**ID:** {dispositivo.get('id', 'N/A')}")
with col2:
    st.write(f"**Localização:** {dispositivo.get('localizacao', 'Não informada')}")
    if dispositivo.get("created_at"):
        st.write(f"**Criado em:** {format_datetime(dispositivo['created_at'])}")

st.markdown("---")

st.subheader("🎯 Finalidade")
st.write(f"**Nome:** {finalidade.get('nome', 'N/A')}")
st.write(f"**Descrição:** {finalidade.get('descricao', 'N/A')}")
st.write(f"**Base Legal:** {finalidade.get('base_legal', 'N/A')}")

st.markdown("---")

st.subheader("📊 Tipo de Dado")
st.write(f"**Nome:** {tipo_dado.get('nome', 'N/A')}")
if tipo_dado.get('descricao'):
    st.write(f"**Descrição:** {tipo_dado['descricao']}")

st.markdown("---")

st.subheader("⚙️ Opção de Tratamento")
st.write(f"**Título:** {opcao_tratamento.get('titulo', 'N/A')}")
st.write(f"**Descrição:** {opcao_tratamento.get('descricao', 'N/A')}")
st.write(f"**Chave de Política:** `{opcao_tratamento.get('chave_politica', 'N/A')}`")

st.markdown("---")

# Ações
st.subheader("🔧 Ações")

# Verificar se estamos no modo de confirmação de revogação
confirming_revoke = st.session_state.get(f"confirming_revoke_{permission_id}", False)

if not confirming_revoke:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✏️ Alterar Permissão", use_container_width=True, type="primary"):
            # Armazenar dados atuais para pré-preencher o formulário
            # Incluir o ID da permissão para poder revogá-la antes de criar a nova
            set_edit_permission_data({
                "permission_id": permission_id,  # ID da permissão a ser revogada
                "dispositivo_id": consentimento["dispositivo_id"],
                "finalidade_id": consentimento["finalidade_id"],
                "tipo_de_dado_id": consentimento["tipo_de_dado_id"],
                "opcao_tratamento_id": consentimento["opcao_tratamento_id"],
            })
            st.switch_page("pages/nova_permissao.py")
    
    with col2:
        if st.button("🚫 Revogar Permissão", use_container_width=True, type="secondary"):
            # Ativar modo de confirmação
            st.session_state[f"confirming_revoke_{permission_id}"] = True
            st.rerun()
else:
    # Modo de confirmação ativo
    st.warning("⚠️ Tem certeza que deseja revogar esta permissão?")
    
    col_yes, col_no = st.columns(2)
    
    with col_yes:
        if st.button("✅ Sim, Revogar", use_container_width=True, key="confirm_revoke", type="primary"):
            try:
                # Obter o dispositivo_id antes de revogar para redirecionar corretamente
                dispositivo_id = consentimento["dispositivo_id"]
                api_client.revogar_consentimento(permission_id)
                # Limpar o estado de confirmação
                if f"confirming_revoke_{permission_id}" in st.session_state:
                    del st.session_state[f"confirming_revoke_{permission_id}"]
                st.success("Permissão revogada com sucesso! ✅")
                # Definir o dispositivo selecionado e redirecionar para seus detalhes
                set_selected_device_id(dispositivo_id)
                st.info("Redirecionando para os detalhes do dispositivo...")
                st.switch_page("pages/detalhes_dispositivo.py")
            except api_client.APIError as e:
                # Limpar o estado de confirmação em caso de erro
                if f"confirming_revoke_{permission_id}" in st.session_state:
                    del st.session_state[f"confirming_revoke_{permission_id}"]
                st.error(f"Erro ao revogar permissão: {str(e)}")
            except Exception as e:
                # Limpar o estado de confirmação em caso de erro
                if f"confirming_revoke_{permission_id}" in st.session_state:
                    del st.session_state[f"confirming_revoke_{permission_id}"]
                st.error(f"Erro inesperado: {str(e)}")
    
    with col_no:
        if st.button("❌ Cancelar", use_container_width=True, key="cancel_revoke"):
            # Limpar o estado de confirmação
            if f"confirming_revoke_{permission_id}" in st.session_state:
                del st.session_state[f"confirming_revoke_{permission_id}"]
            st.rerun()
