# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
pgvector は PostgreSQL の拡張なので、通常の PostgreSQL クライアント / SQL でアクセスします。ベクトル型を使う前に `CREATE EXTENSION vector;` が必要です（サンプルコード内で自動実行します）。

- PostgreSQL: localhost:5432 (user / user)

```bash
$ docker exec -it pgvector psql -U user

# 拡張の有効化
user=# CREATE EXTENSION IF NOT EXISTS vector;

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
(env) $ pip install psycopg2-binary==2.9.10 pgvector==0.3.6
```

# Test
```bash
(env) $ python sample-pgvector.py
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
