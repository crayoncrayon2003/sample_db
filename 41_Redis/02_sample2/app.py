import json
import os
import uuid

import redis
from fastapi import FastAPI, HTTPException, Query

APP_NAME = os.getenv("APP_NAME", "app")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
SESSION_TTL = 1800

app = FastAPI()


def redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def session_key(session_id):
    return "session:{0}".format(session_id)


@app.get("/")
def root():
    return {"app": APP_NAME, "store": "redis", "ttl": SESSION_TTL}


@app.post("/login")
def login(user: str = Query(default="user1")):
    session_id = str(uuid.uuid4())
    payload = {"user": user, "created_by": APP_NAME}

    client = redis_client()
    client.set(session_key(session_id), json.dumps(payload), ex=SESSION_TTL)

    return {"app": APP_NAME, "session_id": session_id, "user": user}


@app.get("/me")
def me(session_id: str):
    client = redis_client()
    value = client.get(session_key(session_id))
    if value is None:
        raise HTTPException(status_code=401, detail="invalid session")

    payload = json.loads(value)
    return {"app": APP_NAME, "session_id": session_id, "session": payload}


@app.delete("/logout")
def logout(session_id: str):
    client = redis_client()
    deleted = client.delete(session_key(session_id))
    return {"app": APP_NAME, "session_id": session_id, "deleted": bool(deleted)}
