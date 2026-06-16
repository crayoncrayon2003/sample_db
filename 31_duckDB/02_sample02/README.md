# 02_sample02: 分位点・分布の形

分位点と分布の形状（歪度・尖度）、度数分布を DuckDB の SQL で求めるサンプルです。
正の歪度を持つ指数分布データを使います。

`sample1.py` の内容:
- `quantile_cont`（補間あり分位点）で四分位点・IQR
- `approx_quantile`（近似分位点。大規模データで高速）
- `skewness`（歪度）・`kurtosis`（尖度）で分布の形
- `floor(value / 幅)` ＋ `GROUP BY` で度数分布（ヒストグラム）

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
