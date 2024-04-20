from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import re 

from ipaddress import ip_address

from typing import Callable

from src.routes import contacts, auth, users
from src.conf.config import config
from src.database.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" Ban/Block Functional
banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2"), ip_address("127.0.0.1")]
user_agent_ban_list = [r"Gecko", r"Python-urllib"]
@app.middleware("http")
async def ban_ips(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip in banned_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response

@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response """

BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath('src').joinpath('static')
app.mount("/static", StaticFiles(directory=directory), name='static')

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0,password=config.REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

templates = Jinja2Templates(directory='src/templates')


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:

        # Make request
        result =  await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Database is not configured correctly"
            )

        return { "message": "Welcome to FastAPI!" }

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Error connecting to the database"
        )