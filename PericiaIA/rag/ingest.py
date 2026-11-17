
from pathlib import Path
import re
import fitz
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"
DB_DIR = BASE_DIR / "chroma_db"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOPICS = {
    "nist_computer_forensics.pdf": "forense_computacional",
    "nist_mobile_forensics.pdf": "forense_mobile",
    "swgde_evidence_collection.pdf": "coleta_evidencias",
    "swgde_forensic_examination.pdf": "exame_forense",
    "swgde_cloud_evidence.pdf": "forense_nuvem",
}

print("Carregando modelo de embeddings...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="pericia_digital",
    metadata={"hnsw:space": "cosine"}
)


def limpar_texto(texto):
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def criar_chunks(texto):
    chunks = []
    inicio = 0

    while inicio < len(texto):
        fim = min(inicio + CHUNK_SIZE, len(texto))
        trecho = texto[inicio:fim].strip()

        if trecho:
            chunks.append(trecho)

        if fim == len(texto):
            break

        inicio = fim - CHUNK_OVERLAP

    return chunks


def processar_pdf(caminho):
    documentos = []
    metadados = []
    ids = []

    with fitz.open(caminho) as pdf:
        for pagina_num, pagina in enumerate(pdf, start=1):
            texto = limpar_texto(pagina.get_text())
            if not texto:
                continue

            chunks = criar_chunks(texto)

            for indice, chunk in enumerate(chunks):
                documentos.append(chunk)

                metadados.append({
                    "source": caminho.name,
                    "page": pagina_num,
                    "topic": TOPICS[caminho.name],
                })

                ids.append(
                    f"{caminho.stem}_p{pagina_num}_c{indice}"
                )

    return documentos, metadados, ids


def main():
    arquivos = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not arquivos:
        print("Nenhum PDF encontrado na pasta documents.")
        return

    for arquivo in arquivos:
        if arquivo.name not in TOPICS:
            print(f"Ignorando documento desconhecido: {arquivo.name}")
            continue

        print(f"Processando: {arquivo.name}")

        documentos, metadados, ids = processar_pdf(arquivo)

        if not documentos:
            print("Nenhum texto extraído.")
            continue

        for inicio in range(0, len(documentos), 64):
            fim = inicio + 64

            lote_documentos = documentos[inicio:fim]
            lote_metadados = metadados[inicio:fim]
            lote_ids = ids[inicio:fim]

            embeddings = model.encode(
                lote_documentos,
                normalize_embeddings=True
            ).tolist()

            collection.upsert(
                ids=lote_ids,
                documents=lote_documentos,
                metadatas=lote_metadados,
                embeddings=embeddings,
            )

        print(f"Chunks processados: {len(documentos)}")

    print("Indexação concluída!")
    print(f"Total de chunks no banco: {collection.count()}")


if __name__ == "__main__":
    main()
