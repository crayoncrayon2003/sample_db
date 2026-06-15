# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Qdrant は SQL クライアントを持たず、REST / gRPC API またはクライアントライブラリ経由でアクセスします。

- REST / gRPC API: http://localhost:6333
- gRPC: localhost:6334
- Web UI (ダッシュボード): http://localhost:6333/dashboard

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:6333/healthz

# コレクション一覧
$ curl http://localhost:6333/collections
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install qdrant-client==1.18.0
```

# Test
```bash
(env) $ python sample-qdrant.py
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
