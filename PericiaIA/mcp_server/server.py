
from pathlib import Path
import sys
import fitz
from mcp.server.mcpserver import MCPServer

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from rag.retriever import search_knowledge as buscar

DOCUMENTS_DIR = BASE_DIR / "documents"

TOPICS = {
    "nist_computer_forensics.pdf": "forense_computacional",
    "nist_mobile_forensics.pdf": "forense_mobile",
    "swgde_evidence_collection.pdf": "coleta_evidencias",
    "swgde_forensic_examination.pdf": "exame_forense",
    "swgde_cloud_evidence.pdf": "forense_nuvem",
}

mcp = MCPServer("PericiaIA")


@mcp.tool()
def search_knowledge(query: str, top_k: int = 5) -> dict:
    """Pesquisa trechos relevantes na base de perícia digital."""
    if not query.strip():
        return {"error": "A pergunta não pode estar vazia."}

    if not 1 <= top_k <= 10:
        return {"error": "top_k deve estar entre 1 e 10."}

    resultados = buscar(query, top_k)

    return {
        "query": query,
        "total": len(resultados),
        "results": resultados
    }


@mcp.tool()
def get_document(document_name: str) -> dict:
    """Recupera o texto e os metadados de um documento PDF."""
    if document_name not in TOPICS:
        return {"error": "Documento não encontrado."}

    caminho = DOCUMENTS_DIR / document_name

    if not caminho.is_file():
        return {"error": "Arquivo PDF indisponível."}

    paginas = []

    with fitz.open(caminho) as pdf:
        for numero, pagina in enumerate(pdf, start=1):
            paginas.append({
                "page": numero,
                "text": pagina.get_text()
            })

    return {
        "document": document_name,
        "topic": TOPICS[document_name],
        "total_pages": len(paginas),
        "pages": paginas
    }


@mcp.tool()
def list_topics() -> dict:
    """Lista os tópicos e documentos da base de conhecimento."""
    return {
        "total_documents": len(TOPICS),
        "topics": [
            {
                "document": nome,
                "topic": topico
            }
            for nome, topico in TOPICS.items()
        ]
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
