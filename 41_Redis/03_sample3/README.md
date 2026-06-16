# Redis Queue

Redis の List をジョブキューとして使います。producer がタスクを push し、worker が pop して処理します。

```text
producer.py
    |
 Redis List
    |
worker.py
```

# Up
```bash
$ sudo docker compose up -d
```

# Test
ターミナルを2つ使います。

```bash
# ターミナル1: ワーカーを起動
(env) $ python worker.py

# ターミナル2: タスクを投入
(env) $ python producer.py
```

# Down
```bash
$ sudo docker compose down
```

