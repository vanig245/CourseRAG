import io
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def loadpdf(pdf_bytes: bytes, embedding_model):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    # print(f"Number of pages in pdf: {len(reader.pages)}")

    chunk_texts = [] 
    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size = 1000,
                    chunk_overlap = 200,
                    length_function = len,
                    is_separator_regex= False,
                    )
    if len(reader.pages) > 0:
        for page in reader.pages:
            text = page.extract_text()
            if text:
                texts = text_splitter.split_text(text)
                chunk_texts.extend(texts)

    else: 
        raise ValueError("pdf has no pages. Please try again!")
    

    vector_db = Chroma.from_texts(
        texts = chunk_texts,
        embedding = embedding_model,
    )

    return vector_db, len(chunk_texts)