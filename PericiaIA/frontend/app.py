
import asyncio
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.orchestrator import perguntar

st.set_page_config(
    page_title="PeríciaIA",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background-color: #111c2e;
}
.stChatMessage {
    border: 1px solid #26364a;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔎 PeríciaIA")
    st.caption("Assistente de Perícia Criminal Digital")
    st.divider()

    st.subheader("Tecnologias")
    st.write("LLM: Llama 3.2 3B")
    st.write("RAG: ChromaDB")
    st.write("Ferramentas: MCP")
    st.write("Documentos: 5 PDFs")

    st.divider()

    if st.button("Nova conversa", use_container_width=True):
        st.session_state.mensagens = []
        st.rerun()

st.title("PeríciaIA")
st.caption(
    "Consulte boas práticas de perícia digital "
    "com respostas fundamentadas em documentos técnicos."
)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

        if mensagem.get("sources"):
            with st.expander("Fontes documentais"):
                for fonte in mensagem["sources"]:
                    st.write(
                        f"📄 {fonte['document']} "
                        f"— página {fonte['page']}"
                    )

pergunta = st.chat_input(
    "Digite sua pergunta sobre perícia criminal digital..."
)

if pergunta:
    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos e gerando resposta..."):
            try:
                resultado = asyncio.run(perguntar(pergunta))
                resposta = resultado["answer"]
                fontes = resultado["sources"]
            except Exception:
                resposta = (
                    "Ocorreu um erro ao processar a consulta. "
                    "Verifique o terminal para mais detalhes."
                )
                fontes = []

        st.markdown(resposta)

        if fontes:
            with st.expander(
                f"Fontes documentais ({len(fontes)})"
            ):
                for fonte in fontes:
                    st.write(
                        f"📄 {fonte['document']} "
                        f"— página {fonte['page']}"
                    )

    st.session_state.mensagens.append({
        "role": "assistant",
        "content": resposta,
        "sources": fontes
    })
