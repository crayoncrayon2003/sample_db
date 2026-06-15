# CDC パターン (Debezium → Redis Streams)

アプリは **PostgreSQL に書くだけ**。ES も Redis も知りません。**Debezium Server** が PostgreSQL の WAL (トランザクションログ) を監視して変更を自動で捕捉し、**Redis Streams** に publish します。subscriber がそれを購読して ES へ反映します。

- ✅ アプリは同期を一切意識しない (改修不要)。誰が・どの経路で更新しても (直接 SQL でも) 漏れなく捕捉できる
- ✅ Debezium がブローカーへ publish するので、自前で WAL を読むサーバは不要
- ❌ インフラ (Debezium + ブローカー) が必要で構成が重い。ニアリアルタイム (結果整合性)

1. app.py（書き込む側）は、 PostgreSQL へデータを書く（正データ）。ES も Redis も知らない

2. Debezium が PostgreSQL の WAL（変更ログ）を監視し、変更を Redis Streams へ publish する

3. subscriber.py は、 Redis Streams から変更を subscribe する

4. subscriber.py は、 変更を Elasticsearch に書き込む（検索用コピー）

5. クライアントは、必要に応じて PostgreSQL／Elasticsearch のデータを読み取る

```
                1 書く（正データ）
   app.py ─────────────────→ (PostgreSQL)   ← 5.クライアントが読む
                                  │
                                  │ 2 WAL を監視して publish
                                  ▼
                            (Debezium Server)
                                  │
                                  ▼
                          (Redis Streams)
                                  │ 3 subscribe
                                  ▼
                            subscriber.py
                                  │ 4 書く（検索用コピー）
                                  ▼
                          (Elasticsearch)   ← 5.クライアントが読む
```

ポイントは、**app.py から出ている矢印は PostgreSQL への1本だけ**で、ES や Redis へは伸びていないこと。sample2 (Queue) では app.py が自分で Redis に push していましたが、CDC では **PostgreSQL の変更ログ**が変更を流すので、app.py は同期を一切書きません。

# Up
Debezium が PostgreSQL に接続してレプリケーションスロット / publication を自動作成します。起動に少し時間がかかります。

```bash
$ sudo docker compose up -d

# Debezium の起動ログ確認 (slot 作成・snapshot 完了まで待つ)
$ docker compose logs -f debezium
```

# Test
仮想環境は親フォルダ (`91_Elasticsearch`) の共通 venv を使います。ターミナルを2つ使います。

```bash
# ターミナル1: subscriber を起動 (Redis Streams を購読)
(env) $ python subscriber.py

# ターミナル2: アプリを実行 (PostgreSQL にだけ書く)
(env) $ python app.py
```

`app.py` は ES のことを一切書いていないのに、ターミナル1の subscriber が `indexed = c 1 Apple MacBook` のように反映します。

# sample1 / sample2 との差: 同期コードが無いのに反映される
読み取りを PostgreSQL / Elasticsearch で分けてあります。

```bash
# 1) PostgreSQL にだけ書く (app.py には ES/Redis のコードは無い)
(env) $ python app.py

# 2) PostgreSQL 側を読む -> すぐにデータがある
(env) $ python read_postgres.py

# 3) Elasticsearch 側を読む -> subscriber.py が拾えば反映されている
(env) $ python read_elasticsearch.py
```

- sample1 (Dual Write) … write.py が **両方に書く**
- sample2 (Queue) … app.py が **Redis に push する**
- sample3 (CDC) … app.py は **PostgreSQL に書くだけ**。あとは Debezium が自動で流す

## CDC の真価: アプリを通さない変更も捕捉する
psql から**直接** UPDATE しても、subscriber が拾って ES に反映されます (app.py を経由しない変更も漏れなく同期される)。

```bash
$ docker exec -it s3-postgres psql -U user -d test \
    -c "UPDATE products SET quantity = 999 WHERE id = 1;"

(env) $ python read_elasticsearch.py
```

# 確認 (curl で直接見る場合)
```bash
$ curl "http://localhost:9200/products/_search?pretty"
```

# Down
```bash
$ sudo docker compose down
```
