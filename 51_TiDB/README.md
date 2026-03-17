# Preparation
```bash
$ mkdir -p data/pd
$ mkdir -p data/tikv
```

# Up
```bash
$ sudo docker compose up -d
```

# Creating Virtual Environment
```bash 
$ python -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install mysql-connector-python
```

# Test
```bash
(env) $ python sample-tidb1.py
(env) $ python sample-tidb2.py
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
$ sudo rm -rf data
$ sudo rm -rf env
```
