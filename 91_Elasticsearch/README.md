# Elasticsearch サンプル集

各サブフォルダは独立した docker-compose 構成のサンプルです。Python の仮想環境 (venv) はこの親フォルダで共通のものを使います。

- `01_sample0` … Elasticsearch 単体の全文検索 (match / fuzzy)
- `01_sample1` … RDB との同期: **Dual Write** (アプリが PostgreSQL と ES の両方に書く)
- `01_sample2` … RDB との同期: **Queue** (アプリが Redis に push → ワーカーが ES へ)
- `01_sample3` … RDB との同期: **CDC** (Debezium が WAL を監視 → Redis Streams → ES。アプリは同期を書かない)
- `01_sample4` … RDB との同期: **Batch** (定期的に PostgreSQL を SELECT して ES へ)

各サンプルの起動・実行手順は、それぞれのフォルダの README.md を参照してください。

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install elasticsearch==8.15.1 psycopg2-binary==2.9.10 redis==5.0.8
```

仮想環境を有効化したまま各サブフォルダに移動してスクリプトを実行します。

```bash
(env) $ cd 01_sample1
(env) $ python app.py
```

# Clean up
```bash
$ sudo rm -rf env
```
