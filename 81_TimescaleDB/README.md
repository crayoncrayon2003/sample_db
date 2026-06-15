# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
TimescaleDB は PostgreSQL の拡張で、時系列データに特化しています。通常の PostgreSQL クライアント / SQL でアクセスし、hypertable や `time_bucket` などの時系列向け機能を使えます。ベクトル型などと同じく、使う前に `CREATE EXTENSION timescaledb;` が必要です（サンプルコード内で自動実行します）。

- PostgreSQL: localhost:5432 (user / user)

```bash
$ docker exec -it timescaledb psql -U user

# 拡張の有効化
user=# CREATE EXTENSION IF NOT EXISTS timescaledb;

# 拡張の確認
user=# \dx

# psql 終了
user=# \q
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
(env) $ python sample1-timescaledb.py

# 特殊な検索: time_bucket で時間ごとに集計 (ダウンサンプリング)
(env) $ python sample2-timescaledb.py
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
