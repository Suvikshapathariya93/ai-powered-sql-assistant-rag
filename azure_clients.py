from functools import lru_cache
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from .config import Settings

@lru_cache(maxsize=1)
def get_openai_client():
    s = Settings()
    return AzureOpenAI(
        azure_endpoint=s.azure_openai_endpoint,
        api_key=s.azure_openai_api_key,
        api_version=s.azure_openai_api_version,
    )

def get_search_index_client():
    s = Settings()
    return SearchIndexClient(endpoint=s.search_endpoint, credential=AzureKeyCredential(s.search_api_key))

def get_search_client():
    s = Settings()
    return SearchClient(endpoint=s.search_endpoint, index_name=s.search_index_name,
                        credential=AzureKeyCredential(s.search_api_key))

def create_embedding(text: str) -> list[float]:
    s = Settings()
    result = get_openai_client().embeddings.create(model=s.embedding_deployment, input=text)
    return result.data[0].embedding

def generate_chat_response(messages: list[dict]) -> str:
    s = Settings()
    result = get_openai_client().chat.completions.create(
        model=s.chat_deployment, messages=messages, temperature=0.2
    )
    return result.choices[0].message.content or ""
