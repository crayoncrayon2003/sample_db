# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
QuestDB は SQL で扱える時系列DBです。PostgreSQL ワイヤ互換 (8812)・InfluxDB line protocol (9009)・REST / Web Console (9000) でアクセスできます。このサンプルでは psycopg2 で PostgreSQL ワイヤに接続し、`SAMPLE BY` などの時系列向け SQL を使います。初期ユーザ / パスワードは admin / quest です。

- Web Console: http://localhost:9000
- PostgreSQL wire: localhost:8812 (admin / quest, db: qdb)
- InfluxDB line protocol: localhost:9009

```bash
# 動作確認 (REST 経由で SQL 実行)
$ curl -G 'http://localhost:9000/exec' --data-urlencode "query=SELECT 1;"
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install psycopg2-binary==2.9.10
```

# Test
```bash
# 基本の時系列データの登録・取得
(env) $ python sample1-questdb.py

# 特殊な検索: SAMPLE BY で時間ごとに集計 (ダウンサンプリング)
(env) $ python sample2-questdb.py
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
