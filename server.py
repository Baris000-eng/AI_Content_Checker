import asyncio
import websockets
import json
from ai_model import predict_chunks 

delta = 0.1
# You will implement this
def is_valid(prob_tuple):
    if abs(prob_tuple[0] - prob_tuple[1]) < delta:
        return 2 # yellow
    if prob_tuple[0] < prob_tuple[1]:
        return 1 # green
    return 3 # red

async def handler(ws):
    print("Python WebSocket listening...")

    async for message in ws:
        print("Received list of <p> elements")

        # message is JSON array of strings
        paragraphs = json.loads(message)
        probabilites = predict_chunks(paragraphs)
        results = []
        for p in probabilites:
            results.append(is_valid(p))

        response = json.dumps({
            "results": results
        })

        await ws.send(response)
        print("→ Sent results:", response)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("Server running at ws://127.0.0.1:8765")
        await asyncio.Future()

asyncio.run(main())
