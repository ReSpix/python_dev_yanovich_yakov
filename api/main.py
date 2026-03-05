from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

import db_conn
from routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_conn.create_pool("authors_database")
    await db_conn.create_pool("logs_database")
    yield
    await db_conn.close_all_pools()


logging.basicConfig(level=logging.INFO)
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
