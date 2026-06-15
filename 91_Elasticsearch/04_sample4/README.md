# Batch パターン

アプリは PostgreSQL に書くだけ。一定間隔で PostgreSQL を **SELECT** して ES にまとめて流し込みます。`updated_at` 列を watermark (前回同期時刻) として差分だけを同期します。

- ✅ 最も簡単。アプリ改修不要。cron などで定期実行するだけ
- ❌ リアルタイム性がない (実行間隔ぶんの遅延)。差分管理用の列 (`updated_at`) が必要

1. app.py（書き込む側）は、 PostgreSQL へデータを書く（正データ）。ES は知らない

2. batch_sync.py は、 PostgreSQL を SELECT する（前回同期時刻 watermark より後の差分だけ）

3. batch_sync.py は、 取得した行を Elasticsearch にまとめて書き込む（検索用コピー）

4. クライアントは、必要に応じて PostgreSQL／Elasticsearch のデータを読み取る

```
                1 書く（正データ）
   app.py ─────────────────→ (PostgreSQL)   ← 4.クライアントが読む
                                  ▲
                                  │ 2 SELECT（watermark より後の差分）
                            batch_sync.py（定期実行）
                                  │ 3 bulk で書く（検索用コピー）
                                  ▼
                          (Elasticsearch)   ← 4.クライアントが読む
```

ポイントは、**app.py から出ている矢印は PostgreSQL への1本だけ**で、ES へは伸びていないこと。ES への反映は batch_sync.py が**後で定期的に**まとめて行うので、実行間隔ぶんの遅延があります。

# Up
```bash
$ sudo docker compose up -d
```

# Test
仮想環境は親フォルダ (`91_Elasticsearch`) の共通 venv を使います。

```bash
# 1) テーブル作成 + 初期データ投入 (PostgreSQL のみ)
(env) $ python app.py init

# 2) 差分同期 -> 3 行が ES に入る
(env) $ python batch_sync.py

# 3) もう一度実行 -> 差分なし ("no changes.")
(env) $ python batch_sync.py

# 4) 1 行だけ更新する
(env) $ python app.py update

# 5) 差分同期 -> 更新した 1 行だけが同期される
(env) $ python batch_sync.py
```

watermark は `.watermark` ファイルに保存され、次回はその時刻より後の行だけが対象になります。

# sample1〜3 との差: 同期は「後でまとめて」行われる
読み取りを PostgreSQL / Elasticsearch で分けてあります。

```bash
# 1) PostgreSQL にだけ書く
(env) $ python app.py init

# 2) PostgreSQL 側を読む -> すぐにデータがある
(env) $ python read_postgres.py

# 3) Elasticsearch 側を読む -> まだ空 (batch_sync.py を実行していないため)
(env) $ python read_elasticsearch.py

# 4) バッチ同期を実行する
(env) $ python batch_sync.py

# 5) もう一度 Elasticsearch 側を読む -> 今度はデータがある
(env) $ python read_elasticsearch.py
```

- sample1 (Dual Write) … write.py が **両方に書く**（即時）
- sample2 (Queue) … app.py が **Redis に push** → worker がすぐ反映（ほぼ即時）
- sample3 (CDC) … Debezium が WAL を拾って自動反映（ニアリアルタイム）
- sample4 (Batch) … batch_sync.py の **実行時にまとめて反映**（実行間隔ぶん遅延）

# 確認 (curl で直接見る場合)
```bash
$ curl "http://localhost:9200/products/_search?pretty"
```

# Down
```bash
$ sudo docker compose down
```

# Clean up
```bash
$ rm -f .watermark
```
