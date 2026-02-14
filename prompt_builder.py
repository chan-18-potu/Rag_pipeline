# prompt_builder.py

def build_document_prompt(context, question):
    return f"""
You must answer ONLY from the document content below.

Document Content:
{context}

Question:
{question}
"""

def build_general_prompt(question):
    return f"""
Answer the question using general knowledge.

Question:
{question}
"""
