<div align="center">

# CourseRAG — Dynamic RAG Assistant for PDFs

**Turn any PDF into an interactive, context-aware chat assistant.**

Upload a syllabus, manual, or report and get instant, hallucination-free answers grounded strictly in the document — no more `Ctrl+F` guesswork.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.1_8B-F55036?style=flat)](https://groq.com/)


</div>

---

## Overview

Navigating dense, multi-page documents like course syllabi, technical manuals, or lengthy reports to find a specific detail — *"What's the late submission policy?"* or *"How is the final grade calculated?"* — is slow and frustrating. Keyword search fails the moment you don't know the exact phrasing the author used.

**CourseRAG** solves this with Retrieval-Augmented Generation (RAG): it reads your PDF, breaks it into semantically meaningful chunks, embeds them into an in-memory vector store, and uses an LLM to answer your questions using *only* the relevant retrieved context — giving you fast, accurate, and traceable answers instead of confident-sounding guesses.

Because the vector database is ephemeral and session-based, there's no persistent storage of your documents — everything is processed in memory and discarded when the session ends.

---

## Features

-  **Upload any PDF** — syllabi, manuals, contracts, research papers, reports
-  **Natural language Q&A** — ask questions the way you'd ask a person, not a search engine
-  **Grounded answers** — responses are constrained to the document's actual content, minimizing hallucinations
-  **Fast inference** — powered by Llama 3.1 8B on Groq's LPU inference engine
-  **Privacy-first** — in-memory vector store means no document persistence between sessions
-  **Local embeddings** — uses `all-MiniLM-L6-v2` via HuggingFace, so embedding generation doesn't require an external API call
-  **Zero-friction UI** — clean, single-page interface with drag-and-drop upload and live chat

---

##  How It Works

```
┌──────────────┐     ┌───────────────────┐     ┌──────────────────────┐
│   PDF Upload  │ ──▶ │  Chunk + Embed     │ ──▶ │  In-Memory ChromaDB   │
│  (pypdf)      │     │  (MiniLM-L6-v2)    │     │  Vector Store         │
└──────────────┘     └───────────────────┘     └───────────┬──────────┘
                                                             │
┌──────────────┐     ┌───────────────────┐     ┌───────────▼──────────┐
│  Your Answer  │ ◀── │  Llama 3.1 8B      │ ◀── │  Top-K Relevant       │
│  (Chat UI)    │     │  (Groq Inference)  │     │  Chunks Retrieved     │
└──────────────┘     └───────────────────┘     └───────────────────────┘
```

1. **Ingest** — `docsprocess.py` reads the uploaded PDF byte stream, splits it into overlapping text chunks, and embeds each chunk locally with `sentence-transformers`.
2. **Store** — Chunks and embeddings are loaded into an in-memory ChromaDB collection scoped to the current session.
3. **Retrieve** — When you ask a question, it's embedded and matched against the stored chunks to find the most relevant context.
4. **Generate** — `ask.py` builds a grounded prompt with that context and sends it to Llama 3.1 8B via Groq for a fast, accurate response.

---

##  Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| **Data Handling** | `python-multipart`, `pydantic` |
| **Orchestration** | [LangChain](https://python.langchain.com/) |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) (in-memory) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (`sentence-transformers`) |
| **LLM Inference** | Meta Llama 3.1 8B via [Groq](https://groq.com/) |
| **PDF Parsing** | `pypdf` |
| **Frontend** | HTML5, Vanilla JavaScript (Fetch API), Tailwind CSS, Marked.js |

---

##  Project Structure

```
CourseRAG/
├── __init__.py         # Package initializer
├── main.py             # FastAPI app — routing, endpoints, server entry point
├── docsprocess.py      # PDF parsing, chunking, and vector DB construction
├── ask.py              # Prompt construction, retrieval, and LLM invocation
├── index.html          # Frontend UI — upload + chat interface
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .gitignore          # Files/folders excluded from version control
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- A free API key from [Groq Console](https://console.groq.com/)

### 1. Clone the repository

```bash
git clone https://github.com/vanig245/CourseRAG.git
cd CourseRAG
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_api_key_here
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. Open the app

Navigate to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

> If the `/` route isn't wired up to serve `index.html`, just open the file directly in your browser instead.

---

## Usage

1. **Upload** — Click the upload area and select a PDF.
2. **Process** — Click "Process Document" to chunk the text and build the in-memory vector store.
3. **Chat** — Once processing completes, ask questions naturally: *"Summarize the attendance policy"* or *"What's due in week 6?"*
4. **Iterate** — Ask follow-up questions; each response stays grounded in the uploaded document.

---

## Roadmap

- [ ] Multi-document support (query across several PDFs at once)
- [ ] Persistent, opt-in vector storage for returning users
- [ ] Source citations with page numbers in chat responses
- [ ] Streaming responses for faster perceived latency
- [ ] Support for additional file types (DOCX, PPTX, TXT)
- [ ] Deployable Docker image

---

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

---

<div align="center">

Built with FastAPI, LangChain, and Groq

</div>