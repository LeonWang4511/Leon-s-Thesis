---
title: 1. 資料設計 L9
nav_order: 2
---
# 01 — 資料設計與切分

## 直交設計（Taguchi L9(3³) inner × tension outer × piece outer）

### 因子層次

| 層次 | 因子 | levels | 物理意義 |
|---|---|---|---|
| Inner L9(3³) | speed | 70 / 100 / 130 % | UM2+ feedrate multiplier |
|  | flow | 90 / 100 / 110 % | UM2+ flow multiplier |
|  | temp | 195 / 210 / 225 °C | hotend setpoint |
| Outer (cross) | tension | 2 / 3 / 4 | 螺絲位置（鬆/中/緊）|
| Outer (replicate) | piece | A / B / C | 3 種幾何形狀 |

### L9 Latin Square（temp 作為 cell value）

```
           flow=90    flow=100    flow=110
speed=70 :  195         210         225
speed=100:  210         225         195
speed=130:  225         195         210
```

**代數關係**：`temp_idx = (speed_idx + flow_idx) mod 3`（cyclic Latin Square）

### 81 prints 結構

- 9 個 (s,f,t) Latin Square × 3 tensions × 3 pieces = **81 prints**
- 每個因子 level 出現 27 次（主效應正交）
- temp 完全被 (s, f) 二因子交互作用 alias（**結構性缺陷，詳見 12 章**）

### 27 個唯一 (s, f, t, tension) 組合對應 print_id

| 編號 | 列印速度 | 流率 | 列印溫度 | 張力等級 |
|:---:|:---:|:---:|:---:|:---:|
| 1–3 | 100 % | 100 % | 225 度 | 2 級 |
| 4–6 | 100 % | 110 % | 195 度 | 3 級 |
| 7–9 | 70 % | 100 % | 210 度 | 3 級 |
| 10–12 | 130 % | 100 % | 195 度 | 4 級 |
| 13–15 | 70 % | 110 % | 225 度 | 4 級 |
| 16–18 | 130 % | 110 % | 210 度 | 2 級 |
| 19–21 | 130 % | 90 % | 225 度 | 3 級 |
| 22–24 | 100 % | 90 % | 210 度 | 4 級 |
| 25–27 | 70 % | 90 % | 195 度 | 2 級 |
| 28–30 | 70 % | 110 % | 225 度 | 3 級 |
| 31–33 | 70 % | 100 % | 210 度 | 2 級 |
| 34–36 | 70 % | 90 % | 195 度 | 3 級 |
| 37–39 | 70 % | 90 % | 195 度 | 4 級 |
| 40–42 | 130 % | 90 % | 225 度 | 4 級 |
| 43–45 | 70 % | 110 % | 225 度 | 2 級 |
| 46–48 | 100 % | 110 % | 195 度 | 4 級 |
| 49–51 | 100 % | 90 % | 210 度 | 3 級 |
| 52–54 | 130 % | 110 % | 210 度 | 3 級 |
| 55–57 | 100 % | 90 % | 210 度 | 2 級 |
| 58–60 | 100 % | 100 % | 225 度 | 3 級 |
| 61–63 | 130 % | 90 % | 225 度 | 2 級 |
| 64–66 | 100 % | 100 % | 225 度 | 4 級 |
| 67–69 | 130 % | 100 % | 195 度 | 3 級 |
| 70–72 | 130 % | 100 % | 195 度 | 2 級 |
| 73–75 | 130 % | 110 % | 210 度 | 4 級 |
| 76–78 | 100 % | 110 % | 195 度 | 2 級 |
| 79–81 | 70 % | 100 % | 210 度 | 4 級 |

每 3 件為同一 (s, f, t, tension) 配 A/B/C piece。

## Holdout 設計

| Holdout 類型 | print_ids | n_prints | 設計意圖 |
|---|---|---:|---|
| **internal_holdout** (合計) | 82-99 | 18 | 完全沒進訓練 |
| └ **internal_holdout_param_ood** | 82-90 | 9 | **故意破壞 L9**（新 (s,f,t) 組合）|
| └ **internal_holdout_geom_ood** | 91-99 | 9 | 沿用 L9 但**新幾何 piece** |

## Train/Val/Test split (1-81)

`random_session_split` (seed=12345)：
- **train**: 57 prints
- **id_val**: 16 prints（model selection + bias calibration 用）
- **id_test**: 8 prints（report 用）

## 樣本數總覽 (1 Hz image sampling, 50 Hz encoder)

| Split | n_prints | n_windows | n_images |
|---|---:|---:|---:|
| train_eval | 57 | 14,741 | 14,741 |
| id_val | 16 | 4,408 | 4,408 |
| id_test | 8 | 2,032 | 2,032 |
| internal_holdout | 18 | 3,637 | 3,637 |
| param_ood | 9 | 1,873 | 1,873 |
| geom_ood | 9 | 1,764 | 1,764 |
| **總計 (1-99)** | **99** | **28,455** | **~24,910 unique** |

## Fault dataset (TCN_v1, 另一系列)

- prints 109-149，5 個故障類別 × 8-9 個 print/class
- 編碼器 40ms 取樣（25 Hz），無影像
- 32 個 print 有效，166,106 個 encoder samples，~111 分鐘總錄製
- 詳見 13 章

## 編碼器訊號（4 channels）

| Channel | 物理意義 |
|---|---|
| dpos_m | 主馬達位置增量 (motor encoder delta) |
| dpos_f | filament 位置增量 (filament encoder delta) |
| K_ratio | 比例（filament / motor 的擠出效率指標）|
| slip_rate | 滑動率（K_ratio 衍生）|

採樣率：50 Hz (v17 模型輸入) 或 25 Hz (TCN_v1)
v17 window length: 100 samples = **2 秒**
TCN_v1 window length: 256 samples = **10.24 秒**

## Tension label 編碼

| 物理 tension level | model class index | 標籤 |
|---|---|---|
| 2（鬆）| 0 | "tension 2" |
| 3（中）| 1 | "tension 3" |
| 4（緊）| 2 | "tension 4" |

（早期錯誤把 tension 當常數 1，v1 era。後期已經修正成 2/3/4）

## 設計缺陷標註

⚠️ **(s, f) → temp 確定別名**：見 11、12 章詳細分析。
⚠️ **小樣本**: 14,741 訓練圖 vs ImageNet 1.28M，需特別注意 shortcut learning 風險。
