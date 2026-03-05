from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_pool("blog_db")
    await db.create_pool("logs_db")
    yield
    await db.close_all_pools()


logging.basicConfig(level=logging.INFO)
app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
