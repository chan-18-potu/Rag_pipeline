# query_embedding.py
from embedding_service import embed_texts

def embed_query(query: str):
    return embed_texts([query])
