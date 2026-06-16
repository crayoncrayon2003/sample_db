# DuckDB サンプル集

DuckDB は組み込み型（サーバ不要）の分析DBです。このフォルダでは、DuckDB の基礎に加えて「**統計 × DB**（データをDBから出さずに SQL で統計処理する）」をテーマにしたサンプルを段階的に並べています。

仮想環境 (venv) と依存 (`requirements.txt`) は **この親フォルダで共通** です。各サブフォルダはその共通 venv を使って実行します。

## サブフォルダ一覧

- `00_sample00` … DuckDB 基礎（永続DB / インメモリ、CSV・JSON 取り込み、SQL 変換）
- `01_sample01` … 記述統計（`SUMMARIZE`、平均・中央値・分散・標準偏差）
- `02_sample02` … 分位点・分布の形（`quantile`、`histogram`、歪度・尖度）
- `03_sample03` … 相関・共分散（`corr`、`covar_*`、相関行列）
- `04_sample04` … 線形回帰（最小二乗）を SQL で（`regr_*`）
- `05_sample05` … 仮説検定（DuckDB で集計 → `scipy` で t検定・カイ二乗）
- `06_sample06` … ウィンドウ関数・グループ統計（`rank`/`ntile`、移動平均）
- `07_sample07` … サンプリング・近似集計（`USING SAMPLE`、`approx_*`）

## Creating Virtual Environment
```bash
# この親フォルダ (31_duckDB) で一度だけ作成する
$ python3.12 -m venv env
$ source env/bin/activate
(env) $ pip install --upgrade pip setuptools
(env) $ pip install -r requirements.txt
```

## Test
```bash
# venv を有効化したまま、各サブフォルダで実行する
(env) $ cd 00_sample00
(env) $ python sample1_DBpath.py
(env) $ python sample2_memory.py

(env) $ cd ../01_sample01
(env) $ python sample1.py
```

## Deactivate Virtual Environment
```bash
(env) $ deactivate
```

## Clean up
```bash
$ sudo rm -rf env
```
