# Privacy Control Panel (PCP)

> **Bilingual README** — English version followed by the original Portuguese version.

---

## 🇺🇸 English

A Streamlit application serving as the frontend for the LGPD consent management framework. It allows data subjects to configure granular privacy permissions, register devices, and manage or revoke active consents — materializing the **Control** and **Inform** privacy design strategies.

### Requirements

- Python 3.12+
- The `consent_management_module` (CMM) backend running and accessible.

### Installation

Install dependencies:

```bash
uv sync
```

### Running

Start the Streamlit application:

```bash
uv run streamlit run app.py
```

### Features

- **Login / Register:** Simple email-based authentication for data subjects.
- **New Device:** Register IoT devices to be managed under the consent framework.
- **New Permission:** Configure granular consent permissions for a device, binding a purpose and a treatment strategy (e.g., raw transmission, temporal aggregation, obfuscation).
- **My Devices:** View and manage all registered devices and their active permissions.
- **Permission Details:** View full details of a specific consent record and take actions (modify or revoke).

### Structure

```
privacy_control_panel/
├── app.py                    # Main entry point
├── api_client.py             # HTTP client for the CMM API
├── utils.py                  # Helper functions
├── pages/
│   ├── login.py              # Login / registration page
│   ├── dashboard.py          # Main dashboard page
│   ├── new_device.py
│   ├── new_permission.py
│   ├── my_devices.py
│   └── permission_details.py
└── pyproject.toml
```

---
---

## 🇧🇷 Português

Aplicação Streamlit que serve como frontend para o sistema de gerenciamento de consentimento.

### Requisitos

- Python 3.12+
- Backend `gerenciador_consentimento` rodando e acessível

### Instalação

Instale as dependências:

```bash
uv sync
```

### Execução

Execute a aplicação Streamlit:

```bash
uv run streamlit run app.py
```

### Funcionalidades

- **Login/Registro**: Autenticação simples por email
- **Novo Dispositivo**: Cadastro de dispositivos IoT
- **Nova Permissão**: Configuração de permissões de consentimento
- **Meus Dispositivos**: Visualização e gerenciamento de dispositivos e permissões
- **Detalhes da Permissão**: Visualização completa e ações (alterar/revogar)

### Estrutura

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
