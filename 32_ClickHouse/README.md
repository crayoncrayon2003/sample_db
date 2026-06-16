# ClickHouse

# Up
```bash
$ sudo docker compose up -d
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install clickhouse-connect
```

# Test
```bash
(env) $ python sample-clickhouse1.py
(env) $ python sample-clickhouse2.py
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
