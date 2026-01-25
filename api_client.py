"""
Cliente HTTP para comunicação com a API do gerenciador_consentimento.
"""
import os
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# URL base da API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIError(Exception):
    """Exceção customizada para erros da API."""
    pass


def _make_request(method: str, endpoint: str, **kwargs) -> Any:
    """
    Faz uma requisição HTTP para a API.
    
    Args:
        method: Método HTTP (GET, POST, PATCH, etc.)
        endpoint: Endpoint da API (ex: "/titulares/")
        **kwargs: Argumentos adicionais para requests (json, params, etc.)
    
    Returns:
        Resposta JSON da API
    
    Raises:
        APIError: Se a requisição falhar
    """
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_msg = f"Erro HTTP {response.status_code}"
        try:
            error_detail = response.json().get("detail", str(e))
            error_msg += f": {error_detail}"
        except:
            error_msg += f": {str(e)}"
        raise APIError(error_msg)
    except requests.exceptions.RequestException as e:
        raise APIError(f"Erro ao conectar com a API: {str(e)}")


# ========== Titulares ==========

def get_titular_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Busca um titular pelo email.
    
    Nota: A API não tem endpoint específico para buscar por email,
    então buscamos todos e filtramos no cliente.
    """
    try:
        titulares = _make_request("GET", "/titulares/", params={"skip": 0, "limit": 1000})
        for titular in titulares:
            if titular.get("email") == email:
                return titular
        return None
    except APIError:
        return None


def create_titular(nome: str, email: str) -> Dict[str, Any]:
    """Cria um novo titular."""
    return _make_request("POST", "/titulares/", json={"nome": nome, "email": email})


def get_titular(titular_id: int) -> Dict[str, Any]:
    """Busca um titular pelo ID."""
    return _make_request("GET", f"/titulares/{titular_id}")


# ========== Dispositivos ==========

def create_dispositivo(nome: str, localizacao: Optional[str] = None) -> Dict[str, Any]:
    """Cria um novo dispositivo."""
    data = {"nome": nome}
    if localizacao:
        data["localizacao"] = localizacao
    return _make_request("POST", "/dispositivos/", json=data)


def get_all_dispositivos() -> List[Dict[str, Any]]:
    """Busca todos os dispositivos."""
    return _make_request("GET", "/dispositivos/", params={"skip": 0, "limit": 1000})


def get_dispositivo(dispositivo_id: int) -> Dict[str, Any]:
    """Busca um dispositivo pelo ID."""
    return _make_request("GET", f"/dispositivos/{dispositivo_id}")


# ========== Finalidades ==========

def get_all_finalidades() -> List[Dict[str, Any]]:
    """Busca todas as finalidades."""
    return _make_request("GET", "/finalidades/", params={"skip": 0, "limit": 1000})


# ========== Tipos de Dados ==========

def get_all_tipos_dados() -> List[Dict[str, Any]]:
    """Busca todos os tipos de dados."""
    return _make_request("GET", "/tipos_dados/", params={"skip": 0, "limit": 1000})


# ========== Opções de Tratamento ==========

def get_all_opcoes_tratamento() -> List[Dict[str, Any]]:
    """Busca todas as opções de tratamento."""
    return _make_request("GET", "/opcoes_tratamento/", params={"skip": 0, "limit": 1000})


# ========== Consentimentos ==========

def create_consentimento(
    titular_id: int,
    dispositivo_id: int,
    finalidade_id: int,
    tipo_de_dado_id: int,
    opcao_tratamento_id: int
) -> Dict[str, Any]:
    """Cria um novo registro de consentimento."""
    return _make_request(
        "POST",
        "/consentimentos/",
        json={
            "titular_id": titular_id,
            "dispositivo_id": dispositivo_id,
            "finalidade_id": finalidade_id,
            "tipo_de_dado_id": tipo_de_dado_id,
            "opcao_tratamento_id": opcao_tratamento_id,
        }
    )


def get_consentimentos_por_titular(titular_id: int) -> List[Dict[str, Any]]:
    """Busca todos os consentimentos ativos de um titular."""
    return _make_request("GET", f"/consentimentos/titular/{titular_id}")


def revogar_consentimento(consentimento_id: int) -> Dict[str, Any]:
    """Revoga um consentimento."""
    return _make_request("PATCH", f"/consentimentos/{consentimento_id}/revogar")
