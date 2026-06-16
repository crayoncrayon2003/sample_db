# Redis Pub/Sub

Redis の Pub/Sub を使って、publisher から subscriber へイベント通知を送ります。subscriber が起動している間に届いたメッセージだけ受信します。

```text
publisher.py
    |
 Redis Pub/Sub
    |
subscriber.py
```

# Up
```bash
$ sudo docker compose up -d
```

# Test
ターミナルを2つ使います。先に subscriber を起動してください。

```bash
# ターミナル1: 購読
(env) $ python subscriber.py

# ターミナル2: 発行
(env) $ python publisher.py
```

# Down
```bash
$ sudo docker compose down
```
