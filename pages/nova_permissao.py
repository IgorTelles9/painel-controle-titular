"""
Página para criar uma nova permissão de consentimento.
"""
import streamlit as st
import api_client
from utils import (
    get_current_user,
    get_pending_device,
    clear_pending_device,
    get_edit_permission_data,
    clear_edit_permission_data,
    get_selected_permission_id
)

# Configurar página
st.set_page_config(page_title="Nova Permissão", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")

# Verificar se usuário está logado
current_user = get_current_user()
if not current_user:
    st.switch_page("pages/login.py")

# Limpar estado ao entrar na página (resetar formulário)
# Só manter estado se estivermos em um fluxo ativo (edição ou dispositivo pendente)
if "nova_permissao_active" not in st.session_state:
    # Primeira vez na página ou voltando de outra página - verificar se há fluxo ativo
    pending_device_id_check = get_pending_device()
    edit_data_check = get_edit_permission_data()
    if not pending_device_id_check and not edit_data_check:
        # Não há fluxo ativo, limpar qualquer estado residual
        clear_edit_permission_data()
        # Limpar também pending_device se existir (caso tenha vindo do botão "Nova Permissão")
        clear_pending_device()
    st.session_state["nova_permissao_active"] = True

st.title("🔐 Nova Permissão")
st.markdown("---")

# Botão para voltar
if st.button("← Voltar ao Painel"):
    # Limpar estado ao sair da página (exceto pending_device se veio de criação de dispositivo)
    clear_edit_permission_data()
    if "nova_permissao_active" in st.session_state:
        del st.session_state["nova_permissao_active"]
    # Não limpar pending_device aqui, pois pode ser necessário se voltar de criar dispositivo
    st.switch_page("pages/painel.py")

st.markdown("---")

# Verificar se há dispositivo pendente ou dados de edição
pending_device_id = get_pending_device()
edit_data = get_edit_permission_data()
is_editing = edit_data is not None

# Carregar dados necessários
try:
    dispositivos = api_client.get_all_dispositivos()
    finalidades = api_client.get_all_finalidades()
    tipos_dados = api_client.get_all_tipos_dados()
    opcoes_tratamento = api_client.get_all_opcoes_tratamento()
except api_client.APIError as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"Erro inesperado: {str(e)}")
    st.stop()

# Preparar dados para o formulário
if is_editing:
    st.subheader("✏️ Alterar Permissão")
    # Pré-preencher com dados da permissão sendo editada
    dispositivo_selecionado_id = edit_data.get("dispositivo_id")
    finalidade_selecionada_id = edit_data.get("finalidade_id")
    tipo_dado_selecionado_id = edit_data.get("tipo_de_dado_id")
    opcao_tratamento_selecionada_id = edit_data.get("opcao_tratamento_id")
    # Dispositivo está travado quando editando
    dispositivo_travado = True
else:
    st.subheader("Criar Nova Permissão")
    # Se há dispositivo pendente, pré-selecionar e travar
    if pending_device_id:
        dispositivo_selecionado_id = pending_device_id
        dispositivo_travado = True
        st.info(f"📱 Configurando permissões para o dispositivo selecionado.")
    else:
        dispositivo_selecionado_id = None
        dispositivo_travado = False
    finalidade_selecionada_id = None
    tipo_dado_selecionado_id = None
    opcao_tratamento_selecionada_id = None

# Formulário
with st.form("nova_permissao_form"):
    # Dispositivo
    if dispositivo_travado:
        # Encontrar o dispositivo para mostrar o nome
        dispositivo_atual = next((d for d in dispositivos if d["id"] == dispositivo_selecionado_id), None)
        if dispositivo_atual:
            st.text_input("Dispositivo", value=dispositivo_atual["nome"], disabled=True)
            st.caption("Este campo foi preenchido automaticamente.")
    else:
        if not dispositivos:
            st.error("Nenhum dispositivo cadastrado. Crie um dispositivo primeiro.")
            st.stop()
        
        dispositivo_options = {f"{d['nome']} (ID: {d['id']})": d["id"] for d in dispositivos}
        dispositivo_selecionado = st.selectbox(
            "Dispositivo *",
            options=list(dispositivo_options.keys()),
            index=0,
            key="select_dispositivo"
        )
        dispositivo_selecionado_id = dispositivo_options[dispositivo_selecionado]
    
    st.markdown("---")
    
    # Finalidade
    if not finalidades:
        st.error("Nenhuma finalidade cadastrada no sistema.")
        st.stop()
    
    finalidade_options = {f"{f['nome']}": f["id"] for f in finalidades}
    finalidade_index = 0
    if finalidade_selecionada_id:
        try:
            finalidade_index = list(finalidade_options.values()).index(finalidade_selecionada_id)
        except ValueError:
            pass
    
    finalidade_selecionada = st.selectbox(
        "Finalidade *",
        options=list(finalidade_options.keys()),
        index=finalidade_index,
        help="Escolha a finalidade para a qual o consentimento será concedido.",
        key="select_finalidade"
    )
    finalidade_selecionada_id = finalidade_options[finalidade_selecionada]
    
    st.markdown("---")
    
    # Tipo de Dado
    if not tipos_dados:
        st.error("Nenhum tipo de dado cadastrado no sistema.")
        st.stop()
    
    tipo_dado_options = {f"{t['nome']}": t["id"] for t in tipos_dados}
    tipo_dado_index = 0
    if tipo_dado_selecionado_id:
        try:
            tipo_dado_index = list(tipo_dado_options.values()).index(tipo_dado_selecionado_id)
        except ValueError:
            pass
    
    tipo_dado_selecionado = st.selectbox(
        "Tipo de Dado *",
        options=list(tipo_dado_options.keys()),
        index=tipo_dado_index,
        help="Escolha o tipo de dado que será coletado.",
        key="select_tipo_dado"
    )
    tipo_dado_selecionado_id = tipo_dado_options[tipo_dado_selecionado]
    
    st.markdown("---")
    
    # Opção de Tratamento
    if not opcoes_tratamento:
        st.error("Nenhuma opção de tratamento cadastrada no sistema.")
        st.stop()
    
    opcao_options = {f"{o['titulo']}": o["id"] for o in opcoes_tratamento}
    opcao_index = 0
    if opcao_tratamento_selecionada_id:
        try:
            opcao_index = list(opcao_options.values()).index(opcao_tratamento_selecionada_id)
        except ValueError:
            pass
    
    opcao_selecionada = st.selectbox(
        "Opção de Tratamento *",
        options=list(opcao_options.keys()),
        index=opcao_index,
        help="Escolha como os dados serão tratados.",
        key="select_opcao_tratamento"
    )
    opcao_tratamento_selecionada_id = opcao_options[opcao_selecionada]
    
    st.markdown("---")
    st.caption("* Campos obrigatórios")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        submitted = st.form_submit_button(
            "✏️ Alterar Permissão" if is_editing else "✅ Criar Permissão",
            use_container_width=True,
            type="primary"
        )
    with col2:
        # Botão para atualizar detalhes sem submeter o form
        atualizar_detalhes = st.form_submit_button(
            "🔄 Atualizar Detalhes",
            use_container_width=True,
            type="secondary"
        )

# Mostrar detalhes fora do formulário para atualização dinâmica
# Ler valores atuais dos selectboxes do session_state
st.markdown("---")

# Obter valores atuais dos selectboxes
finalidade_atual = st.session_state.get("select_finalidade")
tipo_dado_atual = st.session_state.get("select_tipo_dado")
opcao_atual = st.session_state.get("select_opcao_tratamento")

# Detalhes da Finalidade
if finalidade_atual and finalidade_atual in finalidade_options:
    finalidade_id_atual = finalidade_options[finalidade_atual]
    finalidade_info_atual = next((f for f in finalidades if f["id"] == finalidade_id_atual), None)
    if finalidade_info_atual:
        with st.expander("ℹ️ Detalhes da Finalidade"):
            st.write(f"**Descrição:** {finalidade_info_atual.get('descricao', 'N/A')}")
            st.write(f"**Base Legal:** {finalidade_info_atual.get('base_legal', 'N/A')}")

# Detalhes do Tipo de Dado
if tipo_dado_atual and tipo_dado_atual in tipo_dado_options:
    tipo_dado_id_atual = tipo_dado_options[tipo_dado_atual]
    tipo_dado_info_atual = next((t for t in tipos_dados if t["id"] == tipo_dado_id_atual), None)
    if tipo_dado_info_atual and tipo_dado_info_atual.get("descricao"):
        with st.expander("ℹ️ Detalhes do Tipo de Dado"):
            st.write(f"**Descrição:** {tipo_dado_info_atual['descricao']}")

# Detalhes da Opção de Tratamento
if opcao_atual and opcao_atual in opcao_options:
    opcao_id_atual = opcao_options[opcao_atual]
    opcao_info_atual = next((o for o in opcoes_tratamento if o["id"] == opcao_id_atual), None)
    if opcao_info_atual:
        with st.expander("ℹ️ Detalhes da Opção de Tratamento"):
            st.write(f"**Descrição:** {opcao_info_atual.get('descricao', 'N/A')}")
            st.write(f"**Chave de Política:** `{opcao_info_atual.get('chave_politica', 'N/A')}`")

# Se o botão "Atualizar Detalhes" foi clicado, apenas recarregar a página
if atualizar_detalhes:
    st.rerun()

# Processar submissão do formulário
if submitted:
        # Usar valores do session_state se disponíveis (valores atuais dos selectboxes)
        if "select_finalidade" in st.session_state:
            finalidade_selecionada_id = finalidade_options[st.session_state["select_finalidade"]]
        if "select_tipo_dado" in st.session_state:
            tipo_dado_selecionado_id = tipo_dado_options[st.session_state["select_tipo_dado"]]
        if "select_opcao_tratamento" in st.session_state:
            opcao_tratamento_selecionada_id = opcao_options[st.session_state["select_opcao_tratamento"]]
        if "select_dispositivo" in st.session_state and not dispositivo_travado:
            dispositivo_selecionado_id = dispositivo_options[st.session_state["select_dispositivo"]]
        
        try:
            # Se estiver editando, primeiro revogar o consentimento anterior
            old_permission_id = None
            if is_editing:
                old_permission_id = edit_data.get("permission_id")
                if old_permission_id:
                    try:
                        api_client.revogar_consentimento(old_permission_id)
                        st.info("🔄 Permissão anterior revogada.")
                    except api_client.APIError as e:
                        st.warning(f"⚠️ Aviso: Não foi possível revogar a permissão anterior: {str(e)}")
                        st.info("Continuando com a criação da nova permissão...")
            
            # Criar novo consentimento
            novo_consentimento = api_client.create_consentimento(
                titular_id=current_user["id"],
                dispositivo_id=dispositivo_selecionado_id,
                finalidade_id=finalidade_selecionada_id,
                tipo_de_dado_id=tipo_dado_selecionado_id,
                opcao_tratamento_id=opcao_tratamento_selecionada_id
            )
            
            # Limpar dados pendentes
            clear_pending_device()
            clear_edit_permission_data()
            
            # Limpar permissão selecionada se estava editando
            if is_editing and "selected_permission_id" in st.session_state:
                del st.session_state["selected_permission_id"]
            
            # Limpar flag de página ativa para resetar na próxima vez
            if "nova_permissao_active" in st.session_state:
                del st.session_state["nova_permissao_active"]
            
            if is_editing:
                st.success("Permissão alterada com sucesso! ✅")
                st.info("A permissão anterior foi revogada e uma nova foi criada.")
            else:
                st.success("Permissão criada com sucesso! 🎉")
            
            st.balloons()
            st.info("Redirecionando para o painel...")
            st.switch_page("pages/painel.py")
            
        except api_client.APIError as e:
            st.error(f"Erro ao criar permissão: {str(e)}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")
