import concurrent.futures
import json
import time

from pymemcache.client.base import Client

MYHOST = "localhost"
MYPORT = 11214
CACHE_KEY = "heavy:user:100"
LOCK_KEY = "lock:heavy:user:100"


def connect_client():
    return Client((MYHOST, MYPORT), connect_timeout=3, timeout=3)


def compute_heavy_value(worker_id):
    print("worker", worker_id, "computing heavy value")
    time.sleep(2)
    return {
        "user_id": 100,
        "name": "alice",
        "score": 98,
        "computed_by": worker_id,
    }


def get_or_compute(worker_id):
    client = connect_client()
    try:
        cached = client.get(CACHE_KEY)
        if cached is not None:
            return worker_id, "hit", json.loads(cached.decode("utf-8"))

        locked = client.add(LOCK_KEY, b"1", expire=5)
        if locked:
            value = compute_heavy_value(worker_id)
            client.set(CACHE_KEY, json.dumps(value).encode("utf-8"), expire=30)
            client.delete(LOCK_KEY)
            return worker_id, "computed", value

        for _ in range(20):
            time.sleep(0.3)
            cached = client.get(CACHE_KEY)
            if cached is not None:
                return worker_id, "waited", json.loads(cached.decode("utf-8"))

        return worker_id, "miss", None
    finally:
        client.close()


def main():
    client = connect_client()
    try:
        client.delete(CACHE_KEY)
        client.delete(LOCK_KEY)
    finally:
        client.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_or_compute, i) for i in range(1, 6)]
        for future in concurrent.futures.as_completed(futures):
            worker_id, status, value = future.result()
            print("worker =", worker_id, "status =", status, "value =", value)


if __name__ == "__main__":
    main()
