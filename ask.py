def generate_answer(question: str, vector_db, llm) -> str:

    retrieved_pdf = vector_db.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in retrieved_pdf])

    prompt = f"""
    You are an AI teaching assistant. Answer the user's question based only on the following context.
    If the answer is not in the context, do not make things up. Just say "I don't know about this topic based on the provided document".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)
    return response.content