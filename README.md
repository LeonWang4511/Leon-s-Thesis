# Leon's Thesis — FDM 多模態監測完整研究歷程

完整 thesis 研究紀錄，包含資料設計、模型演進、實驗指標、shortcut learning 診斷、部署規格等。

## 主要章節（推薦閱讀順序）

1. [總導覽](00_INDEX.md)
2. [資料設計與切分](01_data_design.md)（Taguchi L9, splits, 樣本數）
3. [v17 canonical model](versions/09_v17_canonical_5blk.md)（current best）
4. [v24 部署優化](versions/11_v24_shallow_wide.md)（per-head best, fusion swap, rescue 嘗試）
5. [Shortcut learning 診斷](12_shortcut_learning_diagnosis.md)（★ 核心研究發現）
6. [所有版本主指標彙整](15_all_metrics_summary.md)
7. [經驗總結 + 未來方向](16_lessons_learned.md)

## 完整目錄

### 主章節（root）

- [00 總導覽](00_INDEX.md)
- [01 資料設計](01_data_design.md)
- [02 早期 v1-v10](02_legacy_v1_to_v10.md)
- [12 Shortcut Learning 診斷](12_shortcut_learning_diagnosis.md)
- [13 TCN_v1 故障偵測](13_tcn_v1_fault_detector.md)
- [14 ONNX 部署](14_onnx_deployment.md)
- [15 全指標彙整](15_all_metrics_summary.md)
- [16 經驗總結](16_lessons_learned.md)

### 版本演進（versions/）

- [03 v11 MobileNetV3 系列](versions/03_v11_mobilenet_series.md)
- [04 v12 Fusion 比較](versions/04_v12_fusion_comparison.md)
- [05 v13 MoCo + Clean Data](versions/05_v13_moco_clean_data.md)
- [06 v14 SeqNorm](versions/06_v14_seqnorm_flow.md)
- [07 v15 DINOv2 ViT 引入](versions/07_v15_dinov2_introduction.md)
- [08 v16 DINOv3](versions/08_v16_dinov3.md)
- [09 v17 Canonical (★)](versions/09_v17_canonical_5blk.md)
- [10 v18-v23 擴展](versions/10_v18_to_v23_extensions.md)
- [11 v24 Shallow Wide (★)](versions/11_v24_shallow_wide.md)
- [v1-v6 中文摘要 (legacy)](versions/legacy_v1_to_v6_summary_zh.md)

### 原始資料表（tables/）

- `all_metrics_master.csv` — 179 runs × 全 head × 全 subset 完整指標
- `all_runs_index.csv` — 簡表
- `all_run_configs.csv` — 206 個 run config
- `all_hyperparameters.csv` — 12 個 hyperparam 文件
- `best_per_package.csv` — 每 package 最佳 run
- `legacy_*.csv` — v1-v6 era 358 筆

### 重生成 scripts（scripts/）

- `01_collect_all_metrics.py` — 掃描所有 metrics.json
- `02_collect_configs.py` — 掃描所有 run_config_resolved.json
- `03_generate_docs.py` — 一次產出所有 markdown

## 編碼

所有 .md 與 .csv 均為 **UTF-8 with BOM**，相容 Windows / Excel / 各 AI 工具。

## 研究主軸

| 目標 | 結果 |
|---|---|
| FDM 多頭參數監測（speed/flow/temp/tension）| **per-head best avg4 = 0.77 on holdout** |
| 故障偵測（N0/A1/A2/A3/A4）| TCN_v1 + state machine |
| 部署規格 | ONNX fp16 (29 MB) + RPi5 ≈ 3 FPS |
| **核心 contribution** | **DOE aliasing → ML shortcut learning bridge** |

## License & 引用

本 repo 為個人 thesis 研究紀錄。引用前請聯繫作者。
"""
