import os
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(
    model = "llama-3.1-8b-instant", 
    api_key = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE") 
)

vector_db = Chroma(
    persist_directory = "./knowledge_base",
    embedding_function = embedding_model
)

def chat() -> str:
    question = input("Ask me anything :")
    retrieved_pdf = vector_db.similarity_search(question, k = 4)
    context = "\n\n".join([doc.page_content for doc in retrieved_pdf])

    print(context)

    prompt = f"""
    You are an AI teaching assistant. Answer the user's question based only on the following context from the syllabus.
    If the answer is not in the context, do not make things up. Just say "I don't know about this topic based on the provided syllabus".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = llm.invoke(prompt)
    return response.content

response = chat()
print(response)