# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
VictoriaMetrics は Prometheus 互換の時系列DBです。InfluxDB line protocol・Prometheus remote write・Graphite など複数の方式で取り込めます。クエリは PromQL を拡張した MetricsQL を HTTP API (`/api/v1/query`, `/api/v1/query_range`) 経由で実行します。このサンプルでは line protocol で取り込みます。

- HTTP API / Web UI (vmui): http://localhost:8428

```bash
# 動作確認 (ヘルスチェック)
$ curl http://localhost:8428/health

# MetricsQL を直接実行
$ curl 'http://localhost:8428/api/v1/query?query=metrics'
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install requests==2.32.3
```

# Test
```bash
# 基本: line protocol で取り込み、範囲取得
(env) $ python sample1-victoriametrics.py

# 特殊な検索: avg_over_time で時間窓を集計 (ダウンサンプリング)
(env) $ python sample2-victoriametrics.py
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
