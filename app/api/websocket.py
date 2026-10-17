import traceback
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain_core.messages import HumanMessage
from app.agents.router import agent  # Import our new brain

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected.")

    try:
        while True:
            user_message = await websocket.receive_text()
            print(f"📩 Received: {user_message}")

            # The input for LangGraph is a dictionary with a list of messages
            inputs = {"messages": [HumanMessage(content=user_message)]}

            try:
                # Import the ToolMessage class to identify tool outputs
                from langchain_core.messages import ToolMessage

                async for event in agent.astream(inputs, stream_mode="messages"):
                    message = event[0]

                    # ONLY stream the final AI response, hide the raw tool output
                    if hasattr(message, "content") and message.content:
                        if not isinstance(message, ToolMessage):
                            await websocket.send_text(str(message.content))

                await websocket.send_text("[END_STREAM]")

            except Exception as e:
                error_msg = f" Agent Error: {str(e)}"
                print(error_msg)
                traceback.print_exc()
                await websocket.send_text(error_msg)
                await websocket.send_text("[END_STREAM]")

    except WebSocketDisconnect:
        print("❌ Client disconnected.")