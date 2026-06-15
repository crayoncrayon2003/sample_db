# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Elasticsearch は全文検索エンジンで、REST API・クライアントライブラリ (elasticsearch) 経由でアクセスします。このサンプルでは簡単のためセキュリティ (認証 / TLS) を無効化しています。

- REST API: http://localhost:9200

```bash
# 動作確認
$ curl http://localhost:9200

# インデックス一覧
$ curl http://localhost:9200/_cat/indices?v
```

# Test
```bash
# 基本の全文検索 (match: 関連度順)
(env) $ python sample1-elasticsearch.py

# 特殊な検索: fuzzy (綴り間違いを許容するあいまい検索)
(env) $ python sample2-elasticsearch.py
```

# Down
```bash
$ sudo docker compose down
```