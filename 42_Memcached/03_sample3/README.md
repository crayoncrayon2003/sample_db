# Memcached TTL / Cache Stampede

Memcached の TTL と `add` を使った簡易ロックで、同じ key の再計算が同時に走りすぎる状況を抑えます。

# Up
```bash
$ sudo docker compose up -d
```

# Test
```bash
(env) $ python sample-stampede.py
```

# Deactivate Virtual Environment
```bash
(env) $ deactivate
```

# Down
```bash
$ sudo docker compose down
```