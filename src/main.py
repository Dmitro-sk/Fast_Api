import uvicorn
from fastapi import FastAPI
from src.api.users import router as user_router

app = FastAPI(title="Lab 3 CRUD")

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)