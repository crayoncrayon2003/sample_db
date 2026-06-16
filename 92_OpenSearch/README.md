# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
OpenSearch は Elasticsearch から派生した全文検索エンジンで、REST API・クライアントライブラリ (opensearch-py) 経由でアクセスします。このサンプルでは簡単のためセキュリティプラグイン (認証 / TLS) を無効化しています。91_Elasticsearch とポートが競合しないよう、ホスト側は 9201 に割り当てています。

- REST API: http://localhost:9201

```bash
# 動作確認
$ curl http://localhost:9201

# インデックス一覧
$ curl http://localhost:9201/_cat/indices?v
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install opensearch-py==2.8.0
```

# Test
```bash
# 基本の全文検索 (match: 関連度順)
(env) $ python sample1-opensearch.py

# 特殊な検索: fuzzy (綴り間違いを許容するあいまい検索)
(env) $ python sample2-opensearch.py
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
