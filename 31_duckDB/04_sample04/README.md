# 04_sample04: 線形回帰（最小二乗）を SQL で

DuckDB の `regr_*` 集約関数で、単回帰（最小二乗法）を SQL だけで実行するサンプルです。
MADlib の `linregr`（in-DB 回帰）に近い「データをDBから出さずモデルを当てる」発想です。

`sample1.py` の内容:
- `regr_slope` / `regr_intercept` / `regr_r2`（傾き・切片・決定係数）
- `regr_avgx` / `regr_avgy` / `regr_count`
- 求めた係数を使い、新しい x に対する予測値を SQL で計算

データは `y = 3x + 5 + ノイズ`。slope≈3、intercept≈5 が復元できます。

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
