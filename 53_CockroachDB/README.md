# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
```bash
$ docker exec -it cockroach bash

# SQLクライアント起動
root@cockroach:/cockroach# cockroach sql --insecure

# データベース作成
root@localhost:26257/defaultdb> CREATE DATABASE test;

# ユーザ作成
root@localhost:26257/defaultdb> CREATE USER "user";

# DB権限付与
root@localhost:26257/defaultdb> GRANT ALL ON DATABASE test TO "user";

# test DBにアクセス
root@localhost:26257/defaultdb> USE test;


# スキーマ権限設定
root@localhost:26257/test> GRANT ALL ON SCHEMA public TO "user";

# QLクライアント終了
root@localhost:26257/test> \q

# コンテナ抜ける
root@cockroach:/cockroach# exit
```


# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install psycopg2-binary
```

# Test
```bash
(env) $ python sample-cockroach.py
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
