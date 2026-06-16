import time

from pymemcache.client.base import Client

MYHOST = "localhost"
MYPORT = 11211


def connect_client():
    return Client((MYHOST, MYPORT), connect_timeout=3, timeout=3)


def test_str(client):
    print("--- test str ---")

    client.set("key11", "value11")
    item = client.get("key11")
    print(item.decode())

    client.set("key21", "10")
    item = client.get("key21")
    print(item.decode())

    client.delete("key11")
    client.delete("key21")


def test_counter(client):
    print("--- test counter ---")

    client.set("counter", "0")
    client.incr("counter", 1)
    client.incr("counter", 9)

    item = client.get("counter")
    print(item.decode())

    client.delete("counter")


def test_ttl(client):
    print("--- test ttl ---")

    client.set("key31", "expires", expire=1)
    item = client.get("key31")
    print(item.decode())

    time.sleep(2)
    item = client.get("key31")
    print(item)


def main():
    client = connect_client()
    try:
        test_str(client)
        test_counter(client)
        test_ttl(client)
    finally:
        client.close()


if __name__ == "__main__":
    main()
