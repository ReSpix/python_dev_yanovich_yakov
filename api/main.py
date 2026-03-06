from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import logging

from db import connection
from exceptions import UserNotFoundException
from routes import api_router
from web.routes import web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection.init_db_engines()
    yield


logging.basicConfig(level=logging.INFO)
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(web_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, e: UserNotFoundException):
    raise HTTPException(status_code=404, detail=e.to_dict())
