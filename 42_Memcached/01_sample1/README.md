# Memcached 共有キャッシュ

Web アプリ A/B/C が同じ Memcached を共有します。どのアプリで保存した値も、別のアプリから同じ key で取得できます。

```text
Web app A
Web app B
Web app C
    |
Memcached
```

# Up
```bash
$ sudo docker compose up -d
```

# Test
```bash
$ curl -X PUT "http://localhost:4201/cache/shared-key?value=hello-from-app-a&ttl=300"
$ curl "http://localhost:4202/cache/shared-key"
$ curl "http://localhost:4203/cache/shared-key"
```

# Down
```bash
$ sudo docker compose down
```
