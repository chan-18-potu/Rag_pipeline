# retriever.py
import faiss
import json
import os
import numpy as np
from config import FAISS_INDEX_PATH, BASE_STORAGE_PATH

TOP_K = 5

def load_index():
    return faiss.read_index(FAISS_INDEX_PATH)

def load_user_metadata(user_id):
    user_meta_path = os.path.join(BASE_STORAGE_PATH, user_id, "metadata")
    all_chunks = []

    for file in os.listdir(user_meta_path):
        with open(os.path.join(user_meta_path, file), "r", encoding="utf-8") as f:
            all_chunks.extend(json.load(f))

    return all_chunks

def retrieve_chunks(user_id, query_vector):
    index = load_index()
    distances, indices = index.search(query_vector, TOP_K)

    user_chunks = load_user_metadata(user_id)

    results = []
    for idx in indices[0]:
        if idx < len(user_chunks):
            results.append(user_chunks[idx])

    return results, distances[0]
