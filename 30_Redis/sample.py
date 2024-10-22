import redis

MYHOST = 'localhost'
MYPORT = 6379
MYUSER = 'user'
MYPASS = 'user'
MTDB   = 'sample_db'

def test_str():
    pool = redis.ConnectionPool(host=MYHOST, port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)

    r.set('key11', 'value11')
    item = r.get('key11')
    print(item.decode())

    r.set('key21', 10)
    item = r.get('key21')
    print(item)

    result = r.delete('key11')
    result = r.delete('key21')

def test_list():
    pool = redis.ConnectionPool(host=MYHOST, port=6379, db=1)
    r = redis.StrictRedis(connection_pool=pool)

    r.rpush('key31', 'value32')
    r.rpush('key31', 'value33')
    r.lpush('key31', 'value31')

    item = r.lpop('key31')
    print(item)
    item = r.lpop('key31')
    print(item)
    item = r.lpop('key31')
    print(item)

    item = r.smembers('key31')
    print(item)

    result = r.delete('key31')

def test_set():
    pool = redis.ConnectionPool(host=MYHOST, port=6379, db=2)
    r = redis.StrictRedis(connection_pool=pool)

    r.sadd('key41', 'value41')
    r.sadd('key41', 'value42')
    r.sadd('key41', 'value41')

    item = r.smembers('key41')
    print(item)

    result = r.delete('key41')

def main():
    test_str()
    test_list()
    test_set()


if __name__ == "__main__":
    main()
