# Queue パターン

アプリは PostgreSQL に書いたあと、変更イベントを **Redis の List (キュー) に push** します。ES への反映は別プロセスの**ワーカー**が担当します。

- ✅ アプリと ES 更新を疎結合にできる。ES が遅い/落ちていてもアプリを待たせない。リトライも可能
- ❌ 同期のきっかけ (push) を作るのはアプリ。push を書き忘れると ES は更新されない。別経路 (直接 SQL など) の変更は捕捉できない

1. app.py（書き込む側）は、 PostgreSQL へデータを書く（正データ）

2. app.py（書き込む側）は、 Redisへ、「こういうデータが入ったよ」というメモを push する

3. worker.py は、 Redisから、メモを pop する

4. worker.py は、 メモを Elasticsearch に書き込む

5. クライアントは、必要に応じてPostgreSQL／Elasticsearchのデータを読み取る

```
                ① 書く
   app.py ─────────────────→ (PostgreSQL)   ← 5.クライアントが読む
     │
     │ ② push（メモを入れる）
     ▼
 (Redis キュー)
     │ ③ pop（メモを取り出す）
     ▼
  worker.py
     │ ④ 書く
     ▼
 (Elasticsearch)　← 5.クライアントが読む

```

# Up
```bash
$ sudo docker compose up -d
```

# Test
仮想環境は親フォルダ (`91_Elasticsearch`) の共通 venv を使います。ターミナルを2つ使います。

```bash
# ターミナル1: ワーカーを起動 (キューを待ち受ける)
(env) $ python worker.py

# ターミナル2: アプリを実行 (PostgreSQL に書いてキューに push)
(env) $ python app.py
```

`app.py` を実行すると、ターミナル1のワーカーが順次 `indexed = ...` と表示して ES に反映します。

# sample1 との差: 非同期の遅延を見る
読み取りを PostgreSQL / Elasticsearch で分けてあります。**worker.py を止めた状態**で試すと、Queue パターンの「反映に遅延がある」性質がよく分かります。

```bash
# 0) (ターミナル1の worker.py は一旦止めておく)

# 1) PostgreSQL に書いてキューに push する
(env) $ python app.py

# 2) PostgreSQL 側を読む -> すぐにデータがある
(env) $ python read_postgres.py

# 3) Elasticsearch 側を読む -> まだ空 (worker が処理していないため)
(env) $ python read_elasticsearch.py

# 4) worker.py を起動するとキューを処理して ES に反映される
(env) $ python worker.py

# 5) もう一度 Elasticsearch 側を読む -> 今度はデータがある
(env) $ python read_elasticsearch.py
```

sample1 (Dual Write) では write.py の中で PostgreSQL と ES の両方に書くので、書いた直後にどちらにもデータがあります。sample2 (Queue) では ES への反映が worker.py まで遅れる、という違いです。

# 確認 (curl で直接見る場合)
```bash
$ curl "http://localhost:9200/products/_search?pretty"
```

# Down
```bash
$ sudo docker compose down
```
