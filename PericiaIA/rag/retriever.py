
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "chroma_db"

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_collection(
    name="pericia_digital"
)


def search_knowledge(query: str, top_k: int = 5):
    if not query.strip():
        return []

    embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    encontrados = []

    for texto, metadata, distancia in zip(
        resultados["documents"][0],
        resultados["metadatas"][0],
        resultados["distances"][0]
    ):
        encontrados.append({
            "text": texto,
            "source": metadata["source"],
            "page": metadata["page"],
            "topic": metadata["topic"],
            "similarity": round(1 - distancia, 4)
        })

    return encontrados


if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")

    resultados = search_knowledge(pergunta)

    for indice, resultado in enumerate(resultados, start=1):
        print(f"\n{'=' * 60}")
        print(f"RESULTADO {indice}")
        print(f"Fonte: {resultado['source']}")
        print(f"Página: {resultado['page']}")
        print(f"Tópico: {resultado['topic']}")
        print(f"Similaridade: {resultado['similarity']:.2%}")
        print(f"\n{resultado['text']}")
