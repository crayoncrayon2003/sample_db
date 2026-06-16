# 01_sample01: 記述統計

DuckDB の SQL だけで記述統計を計算するサンプルです。データはDBから出さずに集計します。

`sample1.py` の内容:
- `SUMMARIZE` … 各列の件数・最小/最大・平均・標準偏差・四分位などを自動算出
- 件数・平均・中央値(`median`)・標準偏差(`stddev_samp`)・分散(`var_samp`)・`mad`（中央絶対偏差）
- `GROUP BY` によるグループ別の平均・標準偏差

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
