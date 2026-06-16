# PostgreSQL + Memcached

PostgreSQL を正データ、Memcached を一時キャッシュとして使う cache-aside パターンです。

1回目は PostgreSQL から読み、結果を Memcached に保存します。2回目は Memcached から返ります。

```text
app.py
  |
Memcached  -- miss -->  PostgreSQL
```

# Up
```bash
$ sudo docker compose up -d
```


# Test
```bash
(env) $ python sample-cache-db.py
```

# Deactivate Virtual Environment
```bash
(env) $ deactivate
```

# Down
```bash
$ sudo docker compose down
```

# Clean up
```bash
$ sudo rm -rf env
```
