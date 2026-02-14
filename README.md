RAG PIPELINE 

OVERVIEW
This project implements a Retrieval-Augmented Generation (RAG) pipeline that allows users to upload PDF documents and ask questions.
If the answer exists in the uploaded documents, the system answers from the document.
If the answer does not exist, the system falls back to general knowledge.

The system is designed with a clear separation between OFFLINE (document ingestion) and ONLINE (question answering) phases, following real-world GenAI architecture.

HIGH LEVEL FLOW

OFFLINE (Ingestion):
PDF → Text Extraction → Cleaning → Chunking → Embeddings → FAISS Index → Metadata

ONLINE (Query):
Question → Embedding → FAISS Search → Confidence Check
→ Document-based Answer OR General Knowledge Answer

PROJECT STRUCTURE

Rag_Pipeline/
faiss_index/
index.faiss (auto-generated vector index)

offline_storage/
users/
<user_id>/
files/ (uploaded PDFs)
text/ (optional extracted text)
metadata/ (chunk metadata JSON)

confidence_check.py
config.py
embedding_service.py
faiss_store.py
llm_service.py
offline_pipeline.py
online_pipeline.py
pdf_loader.py
prompt_builder.py
query_embedding.py
retriever.py
text_processing.py
utils.py
streamlit_app.py
.env
README.md

OFFLINE PHASE – DOCUMENT INGESTION

ENTRY POINT:
process_pdf(user_id, pdf_path, document_id)

WHAT IT DOES:

Creates user folders if missing

Reads PDF and extracts text

Normalizes text

Splits text into overlapping chunks

Converts chunks into embeddings

Loads or creates FAISS index

Adds embeddings to FAISS

Saves FAISS index to disk

Stores metadata mapping chunks to vectors

OUTPUT:

faiss_index/index.faiss

metadata JSON per document

document becomes searchable

IMPORTANT:
FAISS stores only vectors.
Text and ownership are stored separately in metadata.

ONLINE PHASE – QUESTION ANSWERING

ENTRY POINT:
answer_question(user_id, question)

WHAT IT DOES:

Converts question into embedding

Searches FAISS index

Retrieves top matching chunks

Applies confidence threshold

If confident:

Builds document-based prompt

Calls LLM

Returns answer from document

If not confident:

Uses general knowledge prompt

Calls LLM

Returns fallback answer

OUTPUT:

Answer text

Source label (Document or General Knowledge)

KEY DESIGN PRINCIPLES

Offline and Online phases are strictly separated

FAISS handles only vector search

LLM handles only reasoning and language generation

Confidence gate prevents hallucination

User data is isolated

Metadata bridges vectors and text

STREAMLIT UI

The project includes a Streamlit UI that:

Uploads PDFs

Generates a session-based user_id

Runs offline ingestion

Accepts questions

Displays answers with source labels

Run with:
streamlit run streamlit_app.py

API AND ENVIRONMENT

API keys are stored in .env file

OpenAI / Perplexity / Local LLMs can be plugged in

Backend is provider-agnostic

CURRENT STATUS

Offline ingestion working

FAISS index verified

Retrieval verified

Confidence-based fallback implemented

UI ready

LLM billing/provider selection pending

EXTENSIONS POSSIBLE

Immediate:

Chat history memory

Document deletion and re-indexing

Hybrid search (BM25 + FAISS)

Better confidence scoring

Advanced:

Agent-based orchestration

Web search fallback

Authentication

Monitoring and evaluation

Production API deployment
