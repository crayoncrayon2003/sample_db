# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
ArangoDB はマルチモデル (ドキュメント / グラフ / キーバリュー) DBで、HTTP API・AQL・クライアントライブラリ (python-arango) 経由でアクセスします。root パスワードは docker-compose.yml の `ARANGO_ROOT_PASSWORD` で設定しています。サンプルコードは test データベースを自動作成します。

- HTTP API / Web UI: http://localhost:8529 (root / password)

```bash
$ docker exec -it arangodb arangosh --server.password password

# データベース一覧
127.0.0.1:8529@_system> db._databases();

# arangosh 終了
127.0.0.1:8529@_system> exit
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install python-arango==7.9.1
```

# Test
```bash
(env) $ python sample-arango.py
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
