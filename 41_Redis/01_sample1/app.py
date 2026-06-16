import os

import redis
from fastapi import FastAPI, HTTPException, Query

APP_NAME = os.getenv("APP_NAME", "app")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI()


def redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.get("/")
def root():
    return {"app": APP_NAME, "store": "redis"}


@app.put("/cache/{key}")
def set_cache(key: str, value: str, ttl: int = Query(default=300, ge=1)):
    client = redis_client()
    client.set(key, value, ex=ttl)
    return {"app": APP_NAME, "key": key, "value": value, "ttl": ttl}


@app.get("/cache/{key}")
def get_cache(key: str):
    client = redis_client()
    value = client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="cache miss")
    return {"app": APP_NAME, "key": key, "value": value, "source": "redis"}


@app.delete("/cache/{key}")
def delete_cache(key: str):
    client = redis_client()
    deleted = client.delete(key)
    return {"app": APP_NAME, "key": key, "deleted": bool(deleted)}
