# Dual Write パターン

アプリが「正データ (PostgreSQL)」と「検索用 (Elasticsearch)」の**両方に自分で書き込む**最もシンプルな同期方式です。同期の責任はアプリ側にあります。

- ✅ シンプルで直感的
- ❌ 片方が失敗すると不整合になる (PostgreSQL は成功・ES は失敗、など)。トランザクションが効かない

ファイルは「書き込み」と「読み取り」を分けてあります。読み取りは **PostgreSQL から** と **Elasticsearch から** で別ファイルにし、どちらに何が入っているか分かるようにしています。

1. write.py（書き込む側）は、 PostgreSQL へデータを書く（正データ）

2. write.py（書き込む側）は、 Elasticsearch へデータを書く（検索用コピー）

3. クライアントは、必要に応じてPostgreSQL／Elasticsearchのデータを読み取る

```
                1 書く（正データ）
   write.py ─────────────────→ (PostgreSQL)   ← 3.クライアントが読む
     │
     │ 2 書く（検索用コピー）
     ▼
 (Elasticsearch)　← 3.クライアントが読む

```

# Up
```bash
$ sudo docker compose up -d
```

# Test
仮想環境は親フォルダ (`91_Elasticsearch`) の共通 venv を使います。

```bash
# 1) 両方に書き込む
(env) $ python write.py

# 2) PostgreSQL 側を読む
(env) $ python read_postgres.py

# 3) Elasticsearch 側を読む
(env) $ python read_elasticsearch.py
```

両方を読むと、同じ内容が PostgreSQL と Elasticsearch の両方に入っていることが確認できます (Dual Write で 2 か所に書いたため)。

# 確認 (curl / psql で直接見る場合)
```bash
# PostgreSQL 側
$ docker exec -it s1-postgres psql -U user -d test -c "SELECT * FROM products;"

# Elasticsearch 側
$ curl "http://localhost:9200/products/_search?pretty"
```

# Down
```bash
$ sudo docker compose down
```
