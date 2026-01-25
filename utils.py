"""
Funções auxiliares para gerenciamento de sessão Streamlit.
"""
import streamlit as st
from typing import Optional, Dict, Any


def get_current_user() -> Optional[Dict[str, Any]]:
    """Retorna o titular logado atual ou None se não houver usuário logado."""
    return st.session_state.get("current_user")


def set_current_user(titular: Dict[str, Any]) -> None:
    """Define o titular logado na sessão."""
    st.session_state["current_user"] = titular


def clear_session() -> None:
    """Limpa todos os dados da sessão."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def get_pending_device() -> Optional[int]:
    """Retorna o ID do dispositivo pendente (criado mas sem permissões configuradas)."""
    return st.session_state.get("pending_device_id")


def set_pending_device(dispositivo_id: int) -> None:
    """Armazena o ID do dispositivo pendente na sessão."""
    st.session_state["pending_device_id"] = dispositivo_id


def clear_pending_device() -> None:
    """Remove o dispositivo pendente da sessão."""
    if "pending_device_id" in st.session_state:
        del st.session_state["pending_device_id"]


def get_selected_permission_id() -> Optional[int]:
    """Retorna o ID da permissão selecionada para visualização."""
    return st.session_state.get("selected_permission_id")


def set_selected_permission_id(permission_id: int) -> None:
    """Armazena o ID da permissão selecionada na sessão."""
    st.session_state["selected_permission_id"] = permission_id


def get_edit_permission_data() -> Optional[Dict[str, Any]]:
    """Retorna os dados da permissão a ser editada."""
    return st.session_state.get("edit_permission_data")


def set_edit_permission_data(data: Dict[str, Any]) -> None:
    """Armazena os dados da permissão a ser editada na sessão."""
    st.session_state["edit_permission_data"] = data


def clear_edit_permission_data() -> None:
    """Remove os dados de edição da sessão."""
    if "edit_permission_data" in st.session_state:
        del st.session_state["edit_permission_data"]


def get_selected_device_id() -> Optional[int]:
    """Retorna o ID do dispositivo selecionado para visualização."""
    return st.session_state.get("selected_device_id")


def set_selected_device_id(device_id: int) -> None:
    """Armazena o ID do dispositivo selecionado na sessão."""
    st.session_state["selected_device_id"] = device_id


def format_datetime(dt_str: str) -> str:
    """
    Formata uma string de datetime para formato legível (DD/MM/YYYY HH:MM).
    
    Args:
        dt_str: String de datetime no formato ISO (ex: "2024-01-15T10:30:00")
    
    Returns:
        String formatada (ex: "15/01/2024 10:30")
    """
    try:
        from datetime import datetime
        # Tenta parsear diferentes formatos
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S%z"]:
            try:
                dt = datetime.strptime(dt_str, fmt)
                return dt.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                continue
        # Se não conseguir parsear, retorna a string original
        return dt_str
    except Exception:
        return dt_str


def show_loading_centered(message: str = "Carregando..."):
    """
    Exibe um indicador de loading centralizado e visível no meio da tela.
    
    Args:
        message: Mensagem a ser exibida junto com o loading
    """
    import streamlit as st
    
    # Criar container com espaçamento vertical grande
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center; align-items: center; min-height: 400px; flex-direction: column;'>
            <div style='text-align: center; padding: 30px; background-color: rgba(31, 119, 180, 0.1); border-radius: 10px; border: 2px solid #1f77b4;'>
                <div style='font-size: 48px; margin-bottom: 20px;'>⏳</div>
                <div style='font-size: 24px; font-weight: bold; color: #1f77b4;'>{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
