# RESEARCH HISTORY — FDM 多模態監測 完整研究歷程

**整理日期**: 2026-05-22
**作者**: Leon（thesis 主導）+ Claude / Codex 協助
**目標**: FDM 3D 列印多頭參數監測 + 故障偵測，達到部署級表現

## 此資料夾結構

```
RESEARCH_HISTORY/
├── 00_INDEX.md                      ← 本檔（總導覽）
├── 01_data_design.md                ← Taguchi L9 直交設計、資料切分、樣本數
├── 02_legacy_v1_to_v10.md           ← v1-v10 早期 MobileNet 嘗試
├── 03_v11_mobilenet_series.md       ← v11* 系列（MobileNetV3 多頭實驗）
├── 04_v12_fusion_comparison.md      ← v12 fusion 大比較（GMU/FiLM/Sum/Concat/Hadamard）
├── 05_v13_moco_clean_data.md        ← v13/v13c/v13d/v13e MoCo + clean data
├── 06_v14_seqnorm_flow.md           ← v14* sequence normalization
├── 07_v15_dinov2_introduction.md    ← v15 DINOv2 ViT 引入
├── 08_v16_dinov3.md                 ← v16 DINOv3 切換
├── 09_v17_canonical_5blk.md         ← v17 5blk 截斷（current canonical）
├── 10_v18_to_v23_extensions.md      ← v18-v23 (augment, attention, ceiling)
├── 11_v24_shallow_wide.md           ← v24 重要工作（per-head, fusion swap, rescue）
├── 12_shortcut_learning_diagnosis.md ← 關鍵研究發現：DOE aliasing → ML shortcut
├── 13_tcn_v1_fault_detector.md      ← TCN_v1 故障偵測 model
├── 14_onnx_deployment.md            ← ONNX 化 + 部署規格
├── 15_all_metrics_summary.md        ← 所有版本主指標彙整
├── 16_lessons_learned.md            ← 經驗總結 + 未來方向
├── tables/                          ← 所有原始 CSV 表格
│   ├── all_metrics_master.csv       ← 179 runs 全頭全 subset 指標
│   ├── all_runs_index.csv           ← 每 run 簡表
│   ├── all_run_configs.csv          ← 206 個 run config
│   ├── all_hyperparameters.csv      ← 12 個 hyperparam 文件
│   ├── best_per_package.csv         ← 每 package 最佳 run
│   ├── legacy_all_experiment_metrics.csv  ← v1-v6 era 358 筆
│   ├── legacy_best_by_version.csv
│   ├── legacy_best_by_version_phase.csv
│   ├── legacy_top30_overall.csv
│   └── legacy_top20_strict_or_cv_splits.csv
├── versions/                        ← 自動產生的個別 version 摘要
└── scripts/                         ← 重新產生本資料夾的 Python scripts
    ├── 01_collect_all_metrics.py
    ├── 02_collect_configs.py
    └── 03_generate_docs.py
```

## 編碼

所有 markdown 與 CSV 均以 **UTF-8 with BOM** 儲存，確保 Windows/Excel 與 AI 工具都能讀。

## 整體版本演進（high-level）

```
v1-v10:    MobileNetV3 + TCN，多頭分類概念建立
v11-v14:   MobileNetV3 各種 fusion / loss / MoCo pretraining 嘗試
v15:       切換至 DINOv2 ViT-S
v16:       切換至 DINOv3 ViT-S
v17:       DINOv3 truncated 5blk + dual branch GMU（★ canonical）
v18-v23:   各種 augmentation / attention / capacity 上限探索
v24:       per-head best deployment + shortcut learning 診斷 + ONNX 化
```

## 目前最佳成果 (內部 holdout)

| 設定 | avg4 | 來源 |
|---|---:|---|
| MobileNet 時代 (v13d) | 0.512 | 04, 05 章 |
| v17_5blk_seed1 (DINOv3 ViT-S) | 0.652 | 09 章 |
| **per-head best mix + bias + rolling20** | **0.771** | **11 章** |

## 主要研究發現

1. **DOE aliasing → ML shortcut** (詳見 12)：原始 L9 設計使 (s,f) → temp 為確定函數，導致 ML 模型走捷徑而非學真實視覺特徵。
2. **Capacity scaling shortcut** (詳見 12)：ViT-B (768-d) 比 ViT-S (384-d) 在 holdout 上**更差**（tension 0.33 vs 0.58），更大 backbone 將 capacity 用於記憶 print-id 而非泛化特徵。
3. **Temp param_ood 結構性無解** (詳見 11)：在 L9 訓練資料下，temp 視覺信號根本不存在於模型 representation。
4. **ONNX 化幾乎無精度損失** (詳見 14)：fp16 量化後 avg4 差距 < 0.001。

## 給未來讀者

- 從 **00 → 01 → 09 → 11 → 12 → 15** 為核心閱讀路徑
- 02-08 是發展歷史，可選讀
- 13, 14 是部署與工程實作

