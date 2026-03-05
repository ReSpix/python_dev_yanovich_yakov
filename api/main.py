from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import logging

import db_conn
from exceptions import UserNotFoundException
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


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, e: UserNotFoundException):
    raise HTTPException(status_code=404, detail=e.to_dict())
