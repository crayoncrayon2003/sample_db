# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Neo4j はグラフDBで、Cypher を Bolt プロトコル / クライアントライブラリ (neo4j) 経由で実行します。初回ログインのユーザ / パスワードは docker-compose.yml の `NEO4J_AUTH` で設定しています。

- Bolt: bolt://localhost:7687 (neo4j / password)
- Web ブラウザ (Neo4j Browser): http://localhost:7474

```bash
$ docker exec -it neo4j cypher-shell -u neo4j -p password

# ノード件数の確認
neo4j@neo4j> MATCH (n) RETURN count(n);

# cypher-shell 終了
neo4j@neo4j> :exit
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install neo4j==5.26.0
```

# Test
```bash
# 基本のグラフ操作 / 経路探索
(env) $ python sample1-neo4j.py

# 特殊な検索: 俳優 -> 出演映画 -> 共演している別の俳優 をたどる
(env) $ python sample2-neo4j.py
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
