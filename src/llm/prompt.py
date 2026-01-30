
from langchain_core.prompts import PromptTemplate

def get_prompt(context, question, output_lang):
    template = f"""You are a helpful chat assistant. Use the retrieved context to answer the user’s question.

    - Base your answer primarily on the provided context.
    - If the context is insufficient, you may use general knowledge, but keep the answer factual.
    - If you truly don’t know, say so honestly.
    - Always answer in {output_lang}.

    Context:
    {context}

    Question:
    {question}

    Answer (in {output_lang}):
    """

    return template