import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def loadpdf():
    reader = PdfReader("AIML SYLLABUS.PDF")
    print(f"Number of pages in pdf: {len(reader.pages)}")

    chunk_texts = [] 

    if len(reader.pages) > 0:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size = 1000,
                    chunk_overlap = 200,
                    length_function = len,
                    is_separator_regex= False,
                    )
                texts = text_splitter.split_text(text)
                chunk_texts.extend(texts)
                # metadata.extend(texts)
                
        return chunk_texts

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