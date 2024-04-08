from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes import contacts, auth
from src.conf.config import config


from src.database.db import get_db
from sqlalchemy import text
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0,password=config.REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@app.get('/')
def index():
    return {"massage": "Contact Application"}

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