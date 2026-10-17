import asyncio
import websockets


async def test_ai():
    # 1. Connect to our FastAPI WebSocket
    uri = "ws://localhost:8000/ws/chat"
    print("Connecting to server...")

    async with websockets.connect(uri) as websocket:
        # 2. Send a message
        #prompt = "Tell me a short joke about Python programming."
        #prompt = "What is the exact current time?"
        #prompt = "What is the company policy for remote work?"
        prompt = "What is Nina's email address and what is her role?"
        await websocket.send(prompt)
        print(f"\nSent: {prompt}\n")
        print("AI Response: ", end="", flush=True)

        # 3. Listen for the stream
        while True:
            response = await websocket.recv()

            # 4. Check for our end signal
            if response == "[END_STREAM]":
                print("\n\n[Stream Finished]")
                break

            # 5. Print the token immediately (simulating a UI)
            print(response, end="", flush=True)


# Run the async function
if __name__ == "__main__":
    asyncio.run(test_ai())