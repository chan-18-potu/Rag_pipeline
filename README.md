# RAG Pipeline

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that enables users to upload PDF documents and ask questions based on their content.

* If the answer exists within the uploaded documents, the system generates a response grounded in those documents.
* If the answer is not found, the system falls back to general knowledge using an LLM.

The architecture follows real-world Generative AI system design principles with a strict separation between:

* **Offline Phase** – Document ingestion and indexing
* **Online Phase** – Query processing and answer generation

This separation improves scalability, modularity, and maintainability.

---

# Architecture Overview

## High-Level Flow

### Offline (Document Ingestion)

PDF
→ Text Extraction
→ Cleaning & Normalization
→ Chunking (with overlap)
→ Embedding Generation
→ FAISS Vector Indexing
→ Metadata Storage

---

### Online (Question Answering)

User Question
→ Query Embedding
→ FAISS Similarity Search
→ Confidence Evaluation
→ Document-Based Answer
OR
→ General Knowledge Fallback

---

# Project Structure

```
Rag_Pipeline/
│
├── faiss_index/
│   └── index.faiss                # Auto-generated vector index
│
├── offline_storage/
│   └── users/
│       └── <user_id>/
│           ├── files/             # Uploaded PDFs
│           ├── text/              # Extracted text (optional)
│           └── metadata/          # Chunk metadata JSON
│
├── confidence_check.py
├── config.py
├── embedding_service.py
├── faiss_store.py
├── llm_service.py
├── offline_pipeline.py
├── online_pipeline.py
├── pdf_loader.py
├── prompt_builder.py
├── query_embedding.py
├── retriever.py
├── text_processing.py
├── utils.py
├── streamlit_app.py
├── .env
└── README.md
```

---

# Offline Phase – Document Ingestion

### Entry Point

```python
process_pdf(user_id, pdf_path, document_id)
```

### Responsibilities

* Creates user-specific storage directories
* Extracts text from uploaded PDF
* Cleans and normalizes text
* Splits text into overlapping chunks
* Converts chunks into embeddings
* Creates or loads FAISS index
* Stores embeddings in FAISS
* Saves updated FAISS index to disk
* Stores metadata mapping chunks to vector IDs

### Output

* `faiss_index/index.faiss`
* Metadata JSON per document
* Document becomes searchable

> Important:
> FAISS stores only vector embeddings.
> Text content and user ownership are maintained separately in metadata.

---

# Online Phase – Question Answering

### Entry Point

```python
answer_question(user_id, question)
```

### Responsibilities

* Converts question into embedding
* Performs similarity search in FAISS
* Retrieves top matching chunks
* Applies confidence threshold

If confidence is high:

* Builds document-grounded prompt
* Calls LLM
* Returns document-based answer

If confidence is low:

* Uses general knowledge prompt
* Calls LLM
* Returns fallback answer

### Output

* Generated answer
* Source label:

  * `Document`
  * `General Knowledge`

---

# Key Design Principles

* Strict separation between Offline and Online phases
* FAISS handles only vector similarity search
* LLM handles reasoning and natural language generation
* Confidence threshold reduces hallucination risk
* User data isolation per session
* Metadata bridges vector IDs and actual text

---

# Streamlit User Interface

The project includes a Streamlit-based UI that:

* Uploads PDF documents
* Generates a session-based `user_id`
* Executes offline ingestion automatically
* Accepts user questions
* Displays answers with source attribution

### Run the application:

```
streamlit run streamlit_app.py
```

---

# Environment Configuration

* API keys are stored securely in `.env`
* Supports:

  * OpenAI
  * Perplexity
  * Local LLMs
* Backend is provider-agnostic and modular

---

# Current Status

* Offline ingestion: Implemented and tested
* FAISS indexing: Verified
* Retrieval pipeline: Verified
* Confidence-based fallback: Implemented
* Streamlit UI: Functional
* LLM provider billing configuration: Pending

---

# Future Enhancements

## Short-Term Improvements

* Chat history memory
* Document deletion and re-indexing
* Hybrid search (BM25 + FAISS)
* Improved confidence scoring

## Advanced Enhancements

* Agent-based orchestration
* Web search fallback integration
* Authentication and access control
* Monitoring and evaluation metrics
* Production-ready REST API deployment


