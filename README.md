# Interview My AI 🎤🤖

**Interactive AI portfolio tool** that simulates recruiter‑led interviews.  
Visitors can engage with my AI persona in a Q&A format, exploring projects, skills, and technical decisions — all grounded in a custom knowledge base.

---

## 🚀 Features
- **Interview Simulation**: AI acts as the candidate, answering recruiter questions in natural first‑person voice.  
- **Evidence‑Grounded Responses**: Candidate claims backed by a vector knowledge store (no hallucinations).  
- **Retrieval‑Augmented Generation (RAG)**: Combines semantic embeddings + BM25 ranking for precise retrieval.  
- **Dynamic UI**: Streamlit interface for interactive interviews.  
- **Knowledge Ingestion**: PDF, Markdown, Python, and Obsidian vault integration.  
- **Inventory Summarization**: Deterministic overview of all source files/projects.  
- **Supabase Integration**: Auth, storage, and backend functions.  

---

## 🧠 Tech Stack
- **Frontend/UI**: Streamlit  
- **Agent Framework**: smolagents (ToolCallingAgent)  
- **Models**: OpenRouter (LLMs), Gemini Embedding‑2 (768‑dim)  
- **Retrieval**: VectorKnowledgeStore, Rank‑BM25 hybrid search  
- **Backend**: Supabase (auth, storage, functions)  
- **Data Ingestion**: PyMuPDF (PDF parsing), custom loaders for `.md`, `.txt`, `.py`  
- **Infra**: Uvicorn + Starlette for async services  
- **Knowledge Source**: Obsidian vault integration  

---

---

## 🔑 Core Concepts
- **Tool‑Calling Agents**: Modular AI with controlled tool usage.  
- **Retrieval‑Augmented Generation (RAG)**: Evidence‑based candidate answers.  
- **Semantic Search**: Embedding‑driven retrieval with thresholding.  
- **Grounding Boundaries**: No unsupported claims; missing info acknowledged.  
- **Executive Response Style**: Hook → Highlights → Impact.  

---

## 📌 Topics
`ai, ai-agents, ai-tools, portfolio, career-development, streamlit, obsidian, supabase, semantic-search, ranking, gemini-embeddings, rag, chunking, vectorization, vector-embeddings, vector-math, tool-calling-agents, smolagents-framework, openrouter, knowledge-base`

---

## 📦 Releases
- **v1.0.0** – Initial launch with Streamlit UI, RAG pipeline, and Supabase integration.  
- **v1.1.0** – Added inventory summarization + hybrid retrieval.  

---

## 🛠 Deployment
- Deployable via **Streamlit Cloud** or **Docker + Uvicorn**.  
- CI/CD integration possible with GitHub Actions.  

---

## ✨ Portfolio Purpose
This project serves as a **living AI portfolio**, showcasing:  
- My ability to design advanced retrieval pipelines.  
- Integration of modern AI frameworks with backend services.  
- Professional presentation of technical depth in an interview‑style format.
### 📂 Repository Layout

```text
C:\OBSIDIAN\interview_my_ai\
├── agent/                  # Agent factory, tools, and interview instructions
├── config/                 # Settings, source map, secrets management
├── data/                   # Candidate knowledge base (knowledge.jsonl)
├── ingestion/              # Knowledge ingestion pipeline (scanner, loaders, processor)
├── scripts/                # Helper scripts (e.g., packing codebase)
├── .streamlit/             # Streamlit configuration files
├── ui/                     # Streamlit interview interface components
├── tests/                  # Pytest suite for validation
├── .venv/                  # Virtual environment
├── app.py                  # Streamlit entrypoint
├── .gitignore              # Git ignore rules
├── pack_codebase.example.py# Example packing script
├── packed_codebase.example.txt # Example packed output
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Project dependencies
```
