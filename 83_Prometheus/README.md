# Up
```bash
$ sudo docker compose up -d
```

# DB Sitting
Prometheus は pull 型の時系列DB / 監視システムで、対象の `/metrics` エンドポイントを定期的にスクレイプして収集します。クライアントから直接書き込まないため、このサンプルでは **Pushgateway** にメトリクスを push し、Prometheus がそれをスクレイプする構成にしています。クエリは PromQL を HTTP API (`/api/v1/query`) 経由で実行します。

- Prometheus (Web UI / API): http://localhost:9090
- Pushgateway: http://localhost:9092 (コンテナ内ポート 9091)

```bash
# 動作確認
$ curl http://localhost:9090/-/healthy

# PromQL を直接実行
$ curl 'http://localhost:9090/api/v1/query?query=sample_value'
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install prometheus-client==0.21.1 requests==2.32.3
```

# Test
```bash
# 基本: Pushgateway に push し、最新値を取得
(env) $ python sample1-prometheus.py

# 特殊な検索: PromQL の avg_over_time / sum で集計
(env) $ python sample2-prometheus.py
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
