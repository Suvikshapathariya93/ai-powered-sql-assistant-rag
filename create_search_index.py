from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
)
from src.azure_clients import get_search_index_client
from src.config import Settings

def main():
    s = Settings()
    s.validate()
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="source", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chunk_number", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=s.embedding_dimensions,
            vector_search_profile_name="sql-vector-profile",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="sql-hnsw")],
        profiles=[VectorSearchProfile(
            name="sql-vector-profile",
            algorithm_configuration_name="sql-hnsw",
        )],
    )
    index = SearchIndex(name=s.search_index_name, fields=fields, vector_search=vector_search)
    get_search_index_client().create_or_update_index(index)
    print(f"Created/updated index: {s.search_index_name} (dimensions={s.embedding_dimensions})")

if __name__ == "__main__":
    main()
