import os

from fastapi import FastAPI, HTTPException, Query
from pymemcache.client.base import Client

APP_NAME = os.getenv("APP_NAME", "app")
MEMCACHED_HOST = os.getenv("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = int(os.getenv("MEMCACHED_PORT", "11211"))

app = FastAPI()


def memcached_client():
    return Client((MEMCACHED_HOST, MEMCACHED_PORT), connect_timeout=3, timeout=3)


@app.get("/")
def root():
    return {"app": APP_NAME, "store": "memcached"}


@app.put("/cache/{key}")
def set_cache(key: str, value: str, ttl: int = Query(default=300, ge=1)):
    client = memcached_client()
    try:
        client.set(key, value.encode("utf-8"), expire=ttl)
    finally:
        client.close()

    return {"app": APP_NAME, "key": key, "value": value, "ttl": ttl}


@app.get("/cache/{key}")
def get_cache(key: str):
    client = memcached_client()
    try:
        value = client.get(key)
    finally:
        client.close()

    if value is None:
        raise HTTPException(status_code=404, detail="cache miss")

    return {"app": APP_NAME, "key": key, "value": value.decode("utf-8"), "source": "memcached"}


@app.delete("/cache/{key}")
def delete_cache(key: str):
    client = memcached_client()
    try:
        deleted = client.delete(key)
    finally:
        client.close()

    return {"app": APP_NAME, "key": key, "deleted": bool(deleted)}
