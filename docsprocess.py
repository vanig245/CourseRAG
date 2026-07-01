import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def loadpdf():
    reader = PdfReader("AIML SYLLABUS.PDF")
    print(f"Number of pages in pdf: {len(reader.pages)}")
    if len(reader.pages) > 0:
        page = reader.pages[31]
        text = page.extract_text()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        texts = text_splitter.split_text(text)
        return texts
    else: 
        print("pdf has no pages. Please try again!")
        return None
    
texts = loadpdf()
# print(texts)

if texts:
    print("embedding texts and saving it to chromaDb")

    model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_texts(
        texts = texts,
        embedding = model,
        persist_directory="./knowledge_base"
    )