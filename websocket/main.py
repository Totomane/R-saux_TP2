from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*",], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

counter = 0
ws_connections = []   # liste des WebSockets connectées


@app.get("/")
async def root():
    return FileResponse("static/page.html")

@app.post("/increment")
async def increment():
    global counter
    counter += 1
    print("Counter incremented to", counter)
    await broadcast_counter() # pour que tt les websockets est la nouvelle valeur
    return {"counterValue": counter}


@app.post("/decrement")
async def decrement():
    global counter
    counter -= 1
    print("Counter decremented to", counter)

    await broadcast_counter()
    return {"counterValue": counter}


@app.get("/counter")
async def get_counter():
    global counter
    print("Counter value requested:", counter)
    return {"counterValue": counter}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global ws_connections, counter
    await websocket.accept()
    ws_connections.append(websocket)
    print("New WS client connected")
    await websocket.send_text(json.dumps({"counterValue": counter}))    
    try:
        while True:
            action = await websocket.receive_text()
            if action == "increment":
                counter += 1
            elif action == "decrement":
                counter -= 1
            elif action == "reset":
                counter = 0
            await broadcast_counter()

    except WebSocketDisconnect:
        print("Client disconnected")
        ws_connections.remove(websocket)
    except Exception as e:
        print("Error:", e)


async def broadcast_counter():
    """Envoie la valeur du compteur à tous les clients WebSocket."""
    data = json.dumps({"counterValue": counter})
    for ws in ws_connections:
        await ws.send_text(data)

if __name__ == "__main__":
    try:
        host = "127.0.0.1"
        port = 8000
        print(f"Starting uvicorn server on http://{host}:{port}/")
        uvicorn.run("main:app", host=host, port=port, reload=True)
    except Exception as e:
        print("Failed to start uvicorn.\n", e)
