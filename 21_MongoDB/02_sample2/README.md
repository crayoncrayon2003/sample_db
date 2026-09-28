# MongoDB レプリカセットのサンプル

MongoDB 7.0 のデータ保持ノード2台と、投票専用の Arbiter 1台で `dbrs` を構成します。
以下のコマンドは `21_MongoDB/02_sample2` で実行します。Docker に権限が必要な環境では、`docker compose` に `sudo` を付けてください。

| サービス          | 通常時の役割                  | ホスト側の公開ポート |
| ----------------- | ----------------------------- | -------------------- |
| mongodb-primary   | PRIMARY（優先度3）            | 27017                |
| mongodb-secondary | SECONDARY（優先度2）          | 27018                |
| mongodb-arbiter   | ARBITER（データを保存しない） | 27019                |

サービス名は固定ですが、PRIMARY / SECONDARY の役割は選挙で変わります。
ほかの MongoDB サンプルが同じポートやコンテナ名を使用している場合は、先にそのサンプルを停止してください。

# Up

```bash
docker compose up -d
docker compose ps -a
```

# Preparation

起動後に、レプリカセットを初期化します。`up -d` だけでは初期化されません。

```bash
docker compose exec -T mongodb-primary bash /scripts/mongoinit.sh
```

スクリプトは各ノードへの接続を待ち、未初期化の場合だけ `rs.initiate()` を実行します。
既に初期化済みなら設定とデータを保持します。`mongodb-primary` が PRIMARY、
`mongodb-secondary` が SECONDARY、`mongodb-arbiter` が ARBITER になるまで待機し、
準備が完了しなければエラー終了します。再起動後にも同じコマンドを実行できます。

状態だけを確認する場合:

```bash
docker compose exec -T mongodb-primary mongosh --quiet --eval   'rs.status().members.map(m => ({name: m.name, state: m.stateStr, health: m.health}))'
```

# Creating Virtual Environment

Python のサンプルは Docker ホスト側（このターミナル）で実行します。

```bash
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip setuptools
python -m pip install pymongo
```

# Test

```bash
python sample-mongodb.py
```

`testdb.test_collection` に30件追加し、保存済みのドキュメントを表示します。
実行するたびにデータが追加されます。

接続先は次の URI です。

```text
mongodb://localhost:27017/?replicaSet=dbrs&directConnection=true
```

レプリカセットは `mongodb-primary:27017` などの Docker 内部アドレスをクライアントに返します。
ホスト側から通常のレプリカセット探索を行うと、その名前を解決できず接続に失敗します。
また、内部では全ノードが27017を使うため、ホストの27018・27019を URI に列挙するだけでは解決しません。
このローカルサンプルでは `directConnection=true` で公開ポートに直接接続します。
これは [MongoDB 公式の開発環境向け接続方法](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-targets/) に沿った設定です。

**この接続方法は別ノードへの自動フェイルオーバーを行いません。**
書き込みには接続先の `mongodb-primary` が PRIMARY である必要があります。
自動フェイルオーバーを試す場合は、クライアントも同じ Docker ネットワークで実行し、
内部名を列挙した URI と `replicaSet=dbrs` を使用します（`directConnection=true` は付けません）。

# Troubleshooting

```bash
docker compose ps -a
docker compose logs --tail=100 mongodb-primary mongodb-secondary mongodb-arbiter
```

- `Connection refused` / コンテナが `Exited`: `up -d` とコンテナログを確認します。
- `NotYetInitialized`: Preparation のスクリプトを実行します。
- `mongodb-primary` などの名前解決エラー: ホスト側の URI に `directConnection=true` があるか確認します。
- `not primary` / 初期化待機のタイムアウト: 3台が起動しているか、上記の状態確認コマンドで現在の役割を確認します。
- `AlreadyInitialized`: 修正後の初期化スクリプトは既存設定を再初期化しません。以前の設定が異なる場合は `rs.conf()` を確認してください。

既存のレプリカセット設定を確認するコマンド:

```bash
docker compose exec -T mongodb-primary mongosh --quiet --eval 'rs.conf()'
```

# Deactivate Virtual Environment

```bash
deactivate
```

# Down

```bash
docker compose down --timeout 60
```

`./data` のデータは残ります。次回起動時は再利用されます。

# Clean up

仮想環境だけを削除する場合:

```bash
rm -rf env
```

**DB データもすべて破棄してやり直す場合だけ**、必要なバックアップを取得し、
`docker compose down --timeout 60` の後で実行します。次回は Preparation が必要です。

```bash
sudo rm -rf ./data
```
