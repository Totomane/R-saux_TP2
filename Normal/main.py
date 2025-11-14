from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")
counter = 0
@app.get("/")
async def root():
    return FileResponse("static/page.html")
@app.post("/increment")
async def increment():
    global counter
    counter += 1
    print("Counter incremented to:", counter)
    return {"counterValue": counter}
@app.post("/decrement") 
async def decrement():
    global counter
    counter -= 1
    print("Counter decremented to:", counter)
    return {"counterValue": counter}
@app.get("/counter")
async def get_counter():
    global counter
    print("Counter value requested:", counter)
    return {"counterValue": counter}
if __name__ == "__main__":
    try:
        host = "127.0.0.1"
        port = 8000
        print(f"Starting uvicorn server on http://{host}:{port}/ ")
        uvicorn.run("main:app", host=host, port=port, reload=True)
    except Exception as e:
        print("Failed to start uvicorn.\n", e)