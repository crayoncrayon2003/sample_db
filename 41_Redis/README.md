# install
```
pip3 install redis
```

# up
```
$ sudo service docker start
$ sudo docker compose up -d
$ sudo docker compose down
```

# test
```
python samplepy.py
```

# down
```
$ sudo docker compose down
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
(env) $ pip install redis
```

# Test
```bash
(env) $ python sample.py
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
