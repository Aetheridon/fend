from fastapi import FastAPI

app = FastAPI()

@app.get("/llm")
async def root():
    return {"message": "llm API"}