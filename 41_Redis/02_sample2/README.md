# Redis セッション共有

Web アプリ A で作成したセッションを、Web アプリ B/C からも参照します。ロードバランサ配下で複数アプリが動くときの共有セッションの例です。

```text
Web app A  -- login
Web app B  -- session check
Web app C  -- session check
    |
  Redis
```

# Up
```bash
$ sudo docker compose up -d
```

# Test
```bash
$ curl -X POST "http://localhost:4111/login?user=alice"
$ curl "http://localhost:4112/me?session_id=<SESSION_ID>"
$ curl "http://localhost:4113/me?session_id=<SESSION_ID>"
```

# Down
```bash
$ sudo docker compose down
```
