# Memcached セッション共有

Web アプリ A で作成したセッションを、Web アプリ B/C からも参照します。Memcached は TTL 付きの一時セッション保存先として使えます。

```text
Web app A  -- login
Web app B  -- session check
Web app C  -- session check
    |
Memcached
```

# Up
```bash
$ sudo docker compose up -d
```

# Test
```bash
$ curl -X POST "http://localhost:4211/login?user=alice"
$ curl "http://localhost:4212/me?session_id=<SESSION_ID>"
$ curl "http://localhost:4213/me?session_id=<SESSION_ID>"
```

# Down
```bash
$ sudo docker compose down
```
