# 🤖 Enterprise AI Copilot (Agentic RAG System)

A production-grade, locally-hosted AI backend built with **FastAPI**, **LangGraph**, and **ChromaDB**. This system demonstrates an agentic workflow where an LLM intelligently routes user queries to the appropriate tools (Vector Database for unstructured policies, Mock DB for structured employee data) and streams responses in real-time via WebSockets.

## 🌟 Key Features
- **Agentic Routing:** Uses LangGraph to dynamically decide which tool to call based on user intent.
- **Real-time Streaming:** WebSockets stream tokens token-by-token for a ChatGPT-like UX.
- **RAG (Retrieval-Augmented Generation):** ChromaDB vector database for semantic search over company policies.
- **Privacy-First:** Runs entirely locally using Ollama (Llama 3.2). No external API keys or data leakage.
- **Clean Architecture:** Separated API layer, Agent logic, and Tools.

## ️ Tech Stack
- **Backend:** FastAPI, WebSockets, Uvicorn
- **AI Orchestration:** LangGraph, LangChain
- **Vector Database:** ChromaDB
- **LLM:** Ollama (Llama 3.2) - *Local & Free*
- **Testing:** Custom Async WebSocket Client

## 🏗️ Architecture
```text
[Client] --(WebSocket)--> [FastAPI Server] --> [LangGraph Agent]
                                                      |
                                              +-------+-------+
                                              |               |
                                        [Tool 1: RAG]   [Tool 2: HR DB]
                                        (ChromaDB)      (Mock SQL)