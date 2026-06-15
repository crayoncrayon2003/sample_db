# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Milvus は SQL クライアントを持たず、gRPC API またはクライアントライブラリ (pymilvus) 経由でアクセスします。standalone 構成は etcd・MinIO に依存し、同じ docker compose で一緒に起動します。

- gRPC API: localhost:19530
- ヘルス / メトリクス: http://localhost:9091
- MinIO コンソール: http://localhost:9001 (minioadmin / minioadmin)

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:9091/healthz
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip
(env) $ pip install "setuptools<81"
(env) $ pip install pymilvus==2.5.4
```

# Test
```bash
# 基本のベクトル検索 / フィルタ検索
(env) $ python sample1-milvus.py

# 特殊な検索: 基準の映画に「似ている映画」を探す (レコメンド)
(env) $ python sample2-milvus.py
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
