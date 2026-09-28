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

# DB の初期化（初回起動後に必須）

`docker compose up -d` はサーバを起動しますが、Python サンプルが使用する
`user` ロールと `test` データベースは作成しません。
未作成のまま実行すると `FATAL: role "user" does not exist` になります。

以下は `52_YugabyteDB` ディレクトリで実行します。Docker に権限が必要な環境では
`docker compose` に `sudo` を付けてください。

まず YSQL の準備状態を確認します。初回起動には時間がかかります。
`YSQL Status: Ready` になってから初期化してください。
Compose が起動するため、コンテナ内で `yugabyted start` を再実行する必要はありません。

```bash
docker compose exec -T yugabyte bin/yugabyted status --base_dir=/home/yugabyte/yb_data
```

ロール、DB、スキーマ権限をまとめて初期化します。

```bash
docker compose exec -T yugabyte bin/ysqlsh -h yugabyte -p 5433 -U yugabyte -d yugabyte -v ON_ERROR_STOP=1 < init.sql
```

`init.sql` は存在しないロールと DB だけを作成し、必要な権限を付与します。
再実行しても既存データを削除しません。既存ロールのパスワードは変更しません。

サンプルと同じロール・DBで接続できることを確認します。

```bash
docker compose exec -T -e PGPASSWORD=user yugabyte bin/ysqlsh -h yugabyte -p 5433 -U user -d test -c 'SELECT current_user, current_database();'
```

対話的に SQL を実行する場合:

```bash
docker compose exec yugabyte bin/ysqlsh -h yugabyte -p 5433 -U yugabyte -d test
```

終了は `\q` です。接続できない場合は `docker compose ps -a` と
`docker compose logs --tail=100 yugabyte` を確認してください。

公式資料: [ysqlsh の使用方法](https://docs.yugabyte.com/stable/api/ysqlsh/)

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install psycopg2
```

# Test

上記の DB 初期化後に実行します。SQL と JSONB の各テーブルへ3件ずつ追加して表示します。
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

`data` の削除は DB 全体を破棄します。必要なデータをバックアップし、停止後に実行してください。
削除後の起動では DB の初期化を再実行してください。
```bash
$ sudo rm -rf data
$ sudo rm -rf env
```
