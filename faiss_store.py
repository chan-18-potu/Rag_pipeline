# faiss_store.py
import faiss
import os
import numpy as np
from config import FAISS_INDEX_PATH

def load_or_create_index(embedding_dim):
    if os.path.exists(FAISS_INDEX_PATH):
        return faiss.read_index(FAISS_INDEX_PATH)
    else:
        return faiss.IndexFlatL2(embedding_dim)

def save_index(index):
    faiss.write_index(index, FAISS_INDEX_PATH)
