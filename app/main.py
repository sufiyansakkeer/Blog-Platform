from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.router import auth, comment, post


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Blog Platform API", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"status": "pong running"}
