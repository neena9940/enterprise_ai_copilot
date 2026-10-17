import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Initialize LLM
llm = ChatOllama(model="llama3.2", temperature=0)

# 2. Connect to ChromaDB (Policy Search Tool)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "company_db")
client = chromadb.PersistentClient(path=DB_PATH)
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="company_policies", embedding_function=default_ef)


# --- TOOL 1: Unstructured Data (RAG) ---
@tool
def search_company_policy(query: str) -> str:
    """Searches the company policy database for information on remote work, time off, security, or expenses. Use this for general company rules."""

    if collection.count() == 0:
        return "The policy database is currently empty."

    results = collection.query(query_texts=[query], n_results=1)

    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    else:
        return "I couldn't find a specific policy for that."


# --- TOOL 2: Structured Data (Mock HR Database) ---
# In a real app, this would query a PostgreSQL database!
EMPLOYEE_DB = {
    "alice": "Alice Smith, Chief Technology Officer (CTO), alice.smith@company.com",
    "bob": "Bob Jones, HR Manager, bob.jones@company.com",
    "carlos": "Carlos Garcia, Lead Backend Engineer, carlos.garcia@company.com",
    "nina": "Nina Yousefi, Senior AI Engineer, nina.yousefi@company.com"
}


@tool
def lookup_employee_info(name: str) -> str:
    """Looks up an employee's role and email address in the company directory. Use this when asked about a specific person, their job title, or their email."""
    name = name.lower().split()[0]  # Get the first name

    if name in EMPLOYEE_DB:
        return EMPLOYEE_DB[name]
    else:
        return f"Employee '{name}' not found in the directory."


# 3. Create the Agent with BOTH tools
# LangGraph automatically figures out which tool to use based on the user's question!
tools = [search_company_policy, lookup_employee_info]
agent = create_react_agent(llm, tools)