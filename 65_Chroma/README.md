# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Chroma はベクトルDBで、REST API またはクライアントライブラリ (chromadb) 経由でアクセスします。`HttpClient` でサーバに接続します。

- REST API: http://localhost:8000

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:8000/api/v2/heartbeat
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install chromadb==0.5.23
```

# Test
```bash
# 基本のベクトル検索 / フィルタ検索
(env) $ python sample1-chroma.py

# 特殊な検索: 基準の人物に「似ている人物」を探す (レコメンド)
(env) $ python sample2-chroma.py
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
