# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
JanusGraph は分散グラフDBで、Gremlin (Apache TinkerPop) クエリを WebSocket / クライアントライブラリ (gremlinpython) 経由で実行します。公式イメージは単体で BerkeleyDB + Lucene 構成の Gremlin Server を起動します。

- Gremlin Server (WebSocket): ws://localhost:8182/gremlin

```bash
$ docker exec -it janusgraph ./bin/gremlin.sh

# Gremlin Server に接続
gremlin> :remote connect tinkerpop.server conf/remote.yaml
gremlin> :remote console

# ノード件数の確認
gremlin> g.V().count()

# gremlin console 終了
gremlin> :exit
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install gremlinpython==3.7.2
```

# Test
```bash
# 基本のグラフ操作 / 経路探索
(env) $ python sample1-janusgraph.py

# 特殊な検索: 俳優 -> 出演映画 -> 共演している別の俳優 をたどる
(env) $ python sample2-janusgraph.py
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
