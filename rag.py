from azure.search.documents.models import VectorizedQuery
from .azure_clients import create_embedding, generate_chat_response, get_search_client
from .config import Settings
from .prompts import build_messages

def retrieve_context(question: str) -> list[dict]:
    s = Settings()
    vector = create_embedding(question)
    query = VectorizedQuery(vector=vector, k_nearest_neighbors=s.top_k, fields="content_vector")
    results = get_search_client().search(
        search_text=question,
        vector_queries=[query],
        top=s.top_k,
        select=["content", "source", "chunk_number"],
    )
    return [{
        "content": r.get("content", ""),
        "source": r.get("source", "unknown"),
        "chunk_number": r.get("chunk_number", 0),
        "score": r.get("@search.score"),
    } for r in results]

def answer_question(question: str, history: list[dict] | None = None) -> tuple[str, list[dict]]:
    docs = retrieve_context(question)
    return generate_chat_response(build_messages(question, docs, history)), docs
