import uvicorn
from fastapi import FastAPI

from src.api import auth, categories, motorcycles, profiles, teams, users

app = FastAPI(title="RaceHub API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(categories.router)
app.include_router(teams.router)
app.include_router(motorcycles.router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"status": "ok", "message": "RaceHub API is running"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
