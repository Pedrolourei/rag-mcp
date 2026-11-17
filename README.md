# PeríciaIA — Assistente de Perícia Criminal Digital

## Descrição

O PeríciaIA é um assistente de inteligência artificial desenvolvido para consultar documentos técnicos relacionados à perícia criminal digital.

O projeto utiliza um modelo de linguagem executado localmente, combinado com RAG (Retrieval-Augmented Generation), banco vetorial e ferramentas MCP (Model Context Protocol).

## Tecnologias

- Python 3.11
- Ollama — Llama 3.2 3B
- ChromaDB
- Sentence Transformers
- MCP SDK
- Streamlit
- PyMuPDF

## Funcionalidades

- Consultas em linguagem natural sobre perícia criminal digital.
- Recuperação semântica de trechos de documentos técnicos.
- Integração entre LLM e ferramentas MCP.
- Apresentação de documentos e páginas recuperadas.
- Validação inicial de perguntas com guardrails.
- Interface web local.

## Base de conhecimento

O projeto utiliza cinco documentos técnicos das organizações NIST e SWGDE, abrangendo perícia computacional, dispositivos móveis, coleta de evidências, exames forenses e evidências em nuvem.

## Instalação

Requisitos: Python 3.11 e Ollama instalado.

Criar o ambiente virtual:

```powershell
py -3.11 -m venv .venv
```

Ativar no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependências:

```powershell
python -m pip install -r requirements.txt
```

Baixar o modelo:

```powershell
ollama pull llama3.2:3b
```

Indexar os documentos:

```powershell
python -m rag.ingest
```

Executar a aplicação:

```powershell
python -m streamlit run frontend/app.py
```

Acessar `http://localhost:8501`.

## Ferramentas MCP

- `search_knowledge`: realiza buscas na base vetorial.
- `get_document`: recupera documentos técnicos.
- `list_topics`: lista os assuntos disponíveis.

## Limitações

O PeríciaIA é um protótipo acadêmico. Suas respostas podem apresentar imprecisões e as referências recuperadas ainda não passam por validação automática de sustentação de cada afirmação.

O sistema não substitui profissionais habilitados, procedimentos oficiais de investigação ou laudos periciais.
