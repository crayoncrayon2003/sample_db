# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
InfluxDB は時系列DBで、HTTP API・Flux クエリ・クライアントライブラリ (influxdb-client) 経由でアクセスします。初期ユーザ / 組織 (org) / バケット (bucket) / 管理トークンは docker-compose.yml の `DOCKER_INFLUXDB_INIT_*` で設定しています。

- HTTP API / Web UI: http://localhost:8086 (user / password)
- org: sample-org / bucket: sample-bucket / token: sample-token

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:8086/health
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install influxdb-client==1.48.0
```

# Test
```bash
# 基本の時系列データの書き込み・取得
(env) $ python sample1-influxdb.py

# 特殊な検索: aggregateWindow で時間ごとに集計 (ダウンサンプリング)
(env) $ python sample2-influxdb.py
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
