#!/bin/bash
set -euo pipefail

# 固定時間の sleep ではなく、各ノードが接続を受け付けるまで待つ。
for host in mongodb-primary mongodb-secondary mongodb-arbiter; do
  ready=false
  for attempt in {1..30}; do
    if mongosh "mongodb://${host}:27017/?directConnection=true&serverSelectionTimeoutMS=2000" \
      --quiet --eval 'quit(db.adminCommand({ping: 1}).ok === 1 ? 0 : 1)' >/dev/null 2>&1; then
      ready=true
      break
    fi
    sleep 2
  done
  if [ "$ready" != true ]; then
    echo "接続待機がタイムアウトしました: $host" >&2
    exit 1
  fi
done

mongosh 'mongodb://mongodb-primary:27017/?directConnection=true&serverSelectionTimeoutMS=2000' --quiet --eval '
try {
  const status = rs.status();
  if (status.set !== "dbrs") {
    throw new Error("想定外のレプリカセットです: " + status.set);
  }
  print("dbrs は初期化済みです。既存の設定とデータを保持します。");
} catch (error) {
  if (error.code !== 94) throw error; // NotYetInitialized の場合だけ初期化
  const result = rs.initiate({
    _id: "dbrs",
    members: [
      { _id: 0, host: "mongodb-primary:27017", priority: 3 },
      { _id: 1, host: "mongodb-secondary:27017", priority: 2 },
      { _id: 2, host: "mongodb-arbiter:27017", arbiterOnly: true }
    ]
  });
  if (result.ok !== 1) throw new Error(JSON.stringify(result));
}

const deadline = Date.now() + 120000;
while (Date.now() < deadline) {
  const status = rs.status();
  const members = status.members;
  if (members.some(m => m.name === "mongodb-primary:27017" && m.stateStr === "PRIMARY" && m.health === 1)
      && members.some(m => m.name === "mongodb-secondary:27017" && m.stateStr === "SECONDARY" && m.health === 1)
      && members.some(m => m.name === "mongodb-arbiter:27017" && m.stateStr === "ARBITER" && m.health === 1)) {
    printjson(members.map(m => ({name: m.name, state: m.stateStr})));
    quit(0);
  }
  sleep(1000);
}
printjson(rs.status());
throw new Error("レプリカセットの準備が120秒以内に完了しませんでした。ログと rs.conf() を確認してください。");
'
