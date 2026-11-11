import hashlib
from pathlib import Path
from src.azure_clients import create_embedding, get_search_client
from src.chunking import chunk_text, load_knowledge_files
from src.config import Settings

KNOWLEDGE_DIR = Path(__file__).resolve().parents[1] / "data" / "knowledge_base"

def stable_id(source: str, number: int, content: str) -> str:
    return hashlib.sha256(f"{source}:{number}:{content}".encode("utf-8")).hexdigest()

def main():
    s = Settings()
    s.validate()
    docs = load_knowledge_files(KNOWLEDGE_DIR)
    if not docs:
        print(f"No supported files found in {KNOWLEDGE_DIR}")
        return
    client, batch = get_search_client(), []
    for source, text in docs:
        for number, chunk in enumerate(chunk_text(text, s.chunk_size, s.chunk_overlap)):
            batch.append({
                "id": stable_id(Path(source).name, number, chunk),
                "content": chunk,
                "source": Path(source).name,
                "chunk_number": number,
                "content_vector": create_embedding(chunk),
            })
            if len(batch) == 50:
                result = client.upload_documents(documents=batch)
                if any(not item.succeeded for item in result):
                    raise RuntimeError("One or more chunks failed to upload.")
                print(f"Uploaded {len(batch)} chunks")
                batch = []
    if batch:
        result = client.upload_documents(documents=batch)
        if any(not item.succeeded for item in result):
            raise RuntimeError("One or more chunks failed to upload.")
        print(f"Uploaded {len(batch)} chunks")
    print("Ingestion complete. This starter does not remove stale chunks when source files are deleted.")

if __name__ == "__main__":
    main()
