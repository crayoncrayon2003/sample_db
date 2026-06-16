# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Weaviate はベクトルDBで、REST / gRPC API またはクライアントライブラリ (weaviate-client) 経由でアクセスします。このサンプルでは認証を無効 (匿名アクセス) にし、ベクトルは自分で渡すため vectorizer モジュールは使いません。

- REST API: http://localhost:8080
- gRPC: localhost:50051

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:8080/v1/.well-known/ready

# スキーマ (コレクション) 一覧
$ curl http://localhost:8080/v1/schema
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install weaviate-client==4.9.6
```

# Test
```bash
# 基本のベクトル検索 / フィルタ検索
(env) $ python sample1-weaviate.py

# 特殊な検索: 基準の人物に「似ている人物」を探す (レコメンド)
(env) $ python sample2-weaviate.py
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
