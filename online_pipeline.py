# online_pipeline.py
from query_embedding import embed_query
from retriever import retrieve_chunks
from confidence_check import is_confident
from prompt_builder import build_document_prompt, build_general_prompt
from llm_service import generate_answer

def answer_question(user_id, question):
    query_vector = embed_query(question)

    chunks, distances = retrieve_chunks(user_id, query_vector)

    if chunks and is_confident(distances):
        context = "\n".join([c["text"] for c in chunks])
        prompt = build_document_prompt(context, question)
        answer = generate_answer(prompt)
        source = "Uploaded document"
    else:
        prompt = build_general_prompt(question)
        answer = generate_answer(prompt)
        source = "General knowledge"

    return answer, source
