# Painel de Controle do Titular

Aplicação Streamlit que serve como frontend para o sistema de gerenciamento de consentimento.

## Requisitos

- Python 3.12+
- Backend `gerenciador_consentimento` rodando e acessível

## Instalação

1. Instale as dependências:
```bash
uv sync
```

## Execução

Execute a aplicação Streamlit:

```bash
uv run streamlit run app.py
```
## Funcionalidades

- **Login/Registro**: Autenticação simples por email
- **Novo Dispositivo**: Cadastro de dispositivos IoT
- **Nova Permissão**: Configuração de permissões de consentimento
- **Meus Dispositivos**: Visualização e gerenciamento de dispositivos e permissões
- **Detalhes da Permissão**: Visualização completa e ações (alterar/revogar)

## Estrutura

```
painel_controle_titular/
├── app.py                 # Ponto de entrada principal
├── api_client.py          # Cliente HTTP para API
├── utils.py               # Funções auxiliares
├── pages/
│   ├── login.py           # Página de login/registro
│   ├── painel.py          # Página principal
│   ├── novo_dispositivo.py
│   ├── nova_permissao.py
│   ├── meus_dispositivos.py
│   └── detalhes_permissao.py
└── pyproject.toml
```
