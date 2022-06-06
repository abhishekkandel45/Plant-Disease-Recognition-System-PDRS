from fastapi import FastAPI, UploadFile
import uvicorn

app = FastAPI()

@app.get("/ping")
def ping():
    return "Hello!! This is Abhishek's first API"


@app.post("/predict")
async def predict (
    file: UploadFile = File(...)
):
    return {"result": "success"} 


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)