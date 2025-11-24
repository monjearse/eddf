# 🧩 ARQUITETURA DA SOLUÇÃO — EDDF  
## Estação de Dados de Documentos Fiscais com Agentes Autônomos & Integração ERP

A solução EDDF implementa uma pipeline inteligente para **validação, explicação, correção e integração de documentos fiscais eletrónicos (NFe/NFCe)** utilizando **agentes autônomos**, **LLMs (Gemini)**, **Streamlit**, **SQLite** e um **ERP ASP.NET Core**.

---

# 🏗️ 1. Visão Geral da Arquitetura

A arquitetura combina:

- ✔ **Agentes Inteligentes (IA)**
- ✔ **Validação XSD Oficial NFe 4.00**
- ✔ **Correção automática via LLM**
- ✔ **Integração direta com ERP ASP.NET Core**
- ✔ **Interface Streamlit multipágina**
- ✔ **Persistência dos resultados em SQLite**
- ✔ **Dashboard analítico**

---

# 🧠 2. Componentes Principais

| Componente | Função |
|-----------|--------|
| **Validator Agent** | Valida o XML contra o XSD oficial da NFe 4.00 e extrai contexto fiscal. |
| **Tax Interpreter Agent** | Usa Gemini para explicar erros fiscais e regras tributárias. |
| **Fixer Agent** | Sugere XML corrigido conforme o schema oficial. |
| **Integrator Agent** | Envia o XML validado para o ERP via API REST. |
| **Coordinator Agent** | Orquestra todos os agentes e produz resultado consolidado. |
| **Streamlit (UI)** | Interface multipágina de processamento, histórico, dashboard e ajuda. |
| **SQLite** | Armazena logs de validação e integrações ERP. |
| **ERP.Api (ASP.NET Core)** | API REST que insere documentos fiscais na base SQL Server. |
| **Schemas NFe 4.00** | Validação técnica segundo o padrão SEFAZ. |

---

# 🔄 3. Fluxo Completo da Solução

### **1) Upload do XML no Streamlit**
- O utilizador carrega um ou mais ficheiros XML (NFe/NFCe).

### **2) Validator Agent**
- Verifica estrutura do XML contra o schema SEFAZ.
- Extrai:
  - emitente  
  - destinatário  
  - número da NFe  
  - datas  
  - totais fiscais  

### **3) Tax Interpreter Agent**
- Explica erros fiscais em linguagem de negócio.
- Ajuda na interpretação por parte do utilizador.

### **4) Fixer Agent**
- Tenta corrigir o XML usando Gemini.
- Gera uma nova versão e solicita revalidação.

### **5) Revalidação**
- Se o XML corrigido estiver válido → segue para integração.

### **6) Integrator Agent**
- Envia XML para o ERP usando:
  ```
  POST {ERP_API_BASE}{ERP_API_IMPORT_NFE}
  ```
- Recebe:
  - sucesso/falha  
  - ID do documento inserido  
  - logs de integração  

### **7) Persistência**
- Registos são gravados em SQLite:
  - `resultados` (validação)  
  - `integracoes_erp` (integração)  

### **8) Dashboard**
- Gráficos de estatísticas
- Evolução de erros
- Tendências de integração
- Análise de explicações do LLM

---

# 📁 4. Estrutura de Pastas

```
/eddf
│── agents/
│── pages/
│── validation/
│── schemas/
│── database.py
│── nfe_pipeline.py
│── app.py
│── .env
│── README.md
│── README_ACADEMICO.md
```

---

# 🧠 5. Inteligência por Agente

| Agente | Responsabilidade | LLM | Output |
|-------|------------------|-----|--------|
| **ValidatorAgent** | Validação XSD + contexto fiscal | ❌ | Bool + Lista de Erros |
| **TaxInterpreterAgent** | Explicação fiscal | ✅ | Texto |
| **FixerAgent** | Correção automática do XML | ✅ | XML corrigido |
| **IntegratorAgent** | Envio ao ERP + logging | ❌ | Resposta HTTP |
| **CoordinatorAgent** | Orquestra tudo | Parcial | Resultado completo |

---

# 📡 6. Integração com ERP

A API ERP.Api utiliza ASP.NET Core + Dapper.

### **Endpoint de Importação**
```
POST /api/Xml/importar
```

---

# 🌐 9. Configuração do .env

```ini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash
LLM_TEMPERATURE=0.2

ERP_API_BASE=http://localhost:5256
ERP_API_IMPORT_NFE=/api/Xml/importar

DB_PATH=./nfe_validacao.db
XSD_PATH=./schemas/nfe_v4.00.xsd
```

---

# 🏁 10. Conclusão

A arquitetura EDDF demonstra a integração harmoniosa entre:

- Validação técnica rigorosa  
- Correção automática inteligente  
- Explicação fiscal por LLM  
- Integração real com ERP  
- Dashboard analítico  
- Agentes autónomos especializados

Resultando numa solução modular e aplicável ao mundo real.
