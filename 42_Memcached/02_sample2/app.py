import json
import os
import uuid

from fastapi import FastAPI, HTTPException, Query
from pymemcache.client.base import Client

APP_NAME = os.getenv("APP_NAME", "app")
MEMCACHED_HOST = os.getenv("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = int(os.getenv("MEMCACHED_PORT", "11211"))
SESSION_TTL = 1800

app = FastAPI()


def memcached_client():
    return Client((MEMCACHED_HOST, MEMCACHED_PORT), connect_timeout=3, timeout=3)


def session_key(session_id):
    return "session:{0}".format(session_id)


@app.get("/")
def root():
    return {"app": APP_NAME, "store": "memcached", "ttl": SESSION_TTL}


@app.post("/login")
def login(user: str = Query(default="user1")):
    session_id = str(uuid.uuid4())
    payload = {"user": user, "created_by": APP_NAME}

    client = memcached_client()
    try:
        client.set(session_key(session_id), json.dumps(payload).encode("utf-8"), expire=SESSION_TTL)
    finally:
        client.close()

    return {"app": APP_NAME, "session_id": session_id, "user": user}


@app.get("/me")
def me(session_id: str):
    client = memcached_client()
    try:
        value = client.get(session_key(session_id))
    finally:
        client.close()

    if value is None:
        raise HTTPException(status_code=401, detail="invalid session")

    payload = json.loads(value.decode("utf-8"))
    return {"app": APP_NAME, "session_id": session_id, "session": payload}


@app.delete("/logout")
def logout(session_id: str):
    client = memcached_client()
    try:
        deleted = client.delete(session_key(session_id))
    finally:
        client.close()

    return {"app": APP_NAME, "session_id": session_id, "deleted": bool(deleted)}
