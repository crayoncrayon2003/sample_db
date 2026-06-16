# MariaDB

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
(env) $ python sample-mariadb1.py
(env) $ python sample-mariadb2.py
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
