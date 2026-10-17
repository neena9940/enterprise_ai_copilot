import uvicorn
from fastapi import FastAPI
from app.api.websocket import router as ws_router

# 1. Initialize the FastAPI application
app = FastAPI(
    title="Enterprise AI Copilot",
    description="A production-grade AI backend with WebSocket streaming.",
    version="1.0.0"
)

# 2. Include the WebSocket router
app.include_router(ws_router)

# 3. A simple health check endpoint
@app.get("/")
async def root():
    return {"status": "online", "message": "AI Copilot Backend is running."}

# 4. Run the server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)