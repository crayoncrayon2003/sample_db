# Memcached サンプル集

各サブフォルダは独立した docker-compose 構成のサンプルです。

- `00_sample0` ... Memcached の基本操作 (set / get / counter / TTL)
- `01_sample1` ... Web アプリ A/B/C から共有キャッシュとして使う
- `02_sample2` ... Web アプリ A/B/C でセッションを共有する
- `03_sample3` ... TTL と cache stampede 対策
- `04_sample4` ... PostgreSQL + Memcached の cache-aside パターン

各サンプルの起動・実行手順は、それぞれのフォルダの README.md を参照してください。


# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install pymemcache psycopg2-binary
```

# Deactivate Virtual Environment
```bash
(env) $ deactivate
```

# Clean up
```bash
$ sudo rm -rf env
```
