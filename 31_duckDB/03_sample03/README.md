# 03_sample03: 相関・共分散

変数間の相関・共分散を DuckDB の SQL で計算するサンプルです。
`y` は `x` と強く相関、`z` は独立、というデータを使います。

`sample1.py` の内容:
- `corr`（ピアソンの相関係数）、`covar_samp`/`covar_pop`（標本/母共分散）
- `corr` を組み合わせて 3 変数の**相関行列**を SQL で構築

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
