from fastapi import FastAPI, UploadFile, File
from uvicorn import run

app = FastAPI()

@app.get("/")
def root():
    return "Hello!! This is Abhishek's first API"

@app.post("/prediction")
async def predict(
    file:UploadFile= File(...)
):
   pass

if __name__ == "__main__":
    run(app, host='localhost', port=8000)