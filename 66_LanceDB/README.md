# DB Sitting
LanceDB は組み込み型 (サーバレス) のベクトルDBです。SQLite や DuckDB のようにサーバを起動せず、クライアントライブラリ (lancedb) からローカルのディレクトリ (`./lancedb_data`) にデータを保存します。そのため docker-compose はありません。

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install lancedb==0.17.0
```

# Test
```bash
# 基本のベクトル検索 / フィルタ検索
(env) $ python sample1-lancedb.py

# 特殊な検索: 基準の人物に「似ている人物」を探す (レコメンド)
(env) $ python sample2-lancedb.py
```

# Deactivate Virtual Environment
```bash
(env) $ deactivate
```

# Clean up
```bash
$ sudo rm -rf env
$ rm -rf lancedb_data
```
