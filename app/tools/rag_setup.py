import chromadb
from chromadb.config import Settings

# 1. Initialize ChromaDB (Persistent storage so data survives restarts)
client = chromadb.PersistentClient(path="./company_db")

# 2. Create a collection (Like a table in SQL)
collection = client.get_or_create_collection(name="company_policies")

# 3. Our "Documents" (In real life, these would come from PDFs)
documents = [
    "Employees can work remotely up to 3 days a week. Core hours are 10 AM to 3 PM CET.",
    "To request time off, submit a request via the HR portal at least 2 weeks in advance. You get 25 days of paid leave.",
    "All sensitive data must be encrypted at rest. Never share API keys in plain text. Use the company vault for secrets.",
    "Meals up to €20 per day are reimbursable. Submit receipts via the finance app by the 5th of each month."
]

# 4. IDs for the documents
ids = ["remote_work", "time_off", "security", "expenses"]

# 5. Add to database (Only if empty, to avoid duplicates)
if collection.count() == 0:
    collection.add(
        documents=documents,
        ids=ids
    )
    print("✅ Database initialized with company policies!")
else:
    print("Database already exists.")