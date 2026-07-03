import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


from docsprocess import loadpdf
from ask import generate_answer

load_dotenv()

app = FastAPI(title="CourseRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGroq(
    model = "llama-3.1-8b-instant", 
    api_key = os.environ.get("GROQ_API_KEY") 
)

vector_db = None

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_db
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
        pdf_bytes = await file.read()
        
        vector_db, chunk_count = loadpdf(pdf_bytes, embedding_model)
        
        return {"message": f"Successfully processed '{file.filename}' into {chunk_count} chunks."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not vector_db:
        raise HTTPException(status_code=400, detail="Please upload a PDF document first.")
    
    try:
        final_answer = generate_answer(request.question, vector_db, llm)
        return {"answer": final_answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during generation: {str(e)}")
