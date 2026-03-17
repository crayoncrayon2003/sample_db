# Preparation
```bash
$ mkdir -p data/conf
$ mkdir -p data/data
$ mkdir -p data/logs
```

# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting

手順は正しい。ただし、** SQLクライアント起動 **の接続が定期的に切れる

```bash
$ docker exec -it yugabyte bash

# YugabyteDB起動
[root@yugabyte yugabyte]# bin/yugabyted start --base_dir=/home/yugabyte/yb_data

# 状態確認
[root@yugabyte yugabyte]# bin/yugabyted status

# SQLクライアント起動
[root@yugabyte yugabyte]# ysqlsh -h yugabyte -p 5433 -U yugabyte

# データベース作成
yugabyte=# CREATE DATABASE test;

# ユーザ作成
yugabyte=# CREATE USER "user" WITH PASSWORD 'user';

# DB権限付与
yugabyte=# GRANT ALL PRIVILEGES ON DATABASE test TO "user";

# test DBにアクセス
yugabyte=# \c test
または
yugabyte=# ysqlsh -h yugabyte -p 5433 -U yugabyte -d test

# スキーマ権限設定
test=# GRANT CREATE ON SCHEMA public TO "user";
test=# GRANT ALL ON SCHEMA public TO "user";
test=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
test=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "user";

# スキーマ所有者変更
test=# ALTER SCHEMA public OWNER TO "user";

# QLクライアント終了
test=# \q

# コンテナ抜ける
[root@yugabyte yugabyte]#　exit
```



# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install psycopg2
```

# Test
```bash
(env) $ python sample-postgre.py
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
$ sudo rm -rf data
$ sudo rm -rf env
```
