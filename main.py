from fastapi import FastAPI
from application.routers.router import router
import uvicorn

app = FastAPI(title="SQL RAG API")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)