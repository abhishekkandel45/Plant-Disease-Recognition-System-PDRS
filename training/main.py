from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
def root():
    return "Hello!! This is Abhishek's first API"

if __name__ == "__main__":
    run(app, host='localhost', port=8000)