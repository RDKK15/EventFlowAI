from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "app": "BizPart AI",
        "version": "0.1.0",
        "developer": "Your Name",
        "status": "Running 🚀"
    }