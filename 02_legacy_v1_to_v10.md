---
title: v1-v10 早期
nav_order: 1
parent: 版本演進 (Version History)
---

# v1 - v10 — 早期 MobileNet 嘗試

## 資料來源

`experiment_metrics_audit/` 整理了 v1-v6 共 358 筆實驗 metric。
原始 CSV 已複製到 [`tables/legacy_*.csv`](../tables/).

## 主要技術演進

| 版本 | 主要嘗試 | 結論 |
|---|---|---|
| v1 | MobileNetV3-Small + TCN 多模態 baseline | 確立 image + encoder 雙模態必要性 |
| v2 | 改 preprocessing | 微幅提升 |
| v3-v4 | Source pretraining (Lite CAXTON backbone) | val 上升但 test 提升有限 |
| v5 | 4-head CAXTON source-adapted backbone | 取代 3-head source |
| v5.1-v5.3 | Fusion ablation (M0-M5: image-only, concat, FiLM, cross-attn) | M2 FiLM 略勝 |
| v6 | Tension label 修正（從常數 1 → 真實 2/3/4）+ 全頭訓練 | 重新校準所有比較 |
| v10 | 過渡期，協議統一化 | 為 v11 鋪路 |

## 數據

詳細 358 runs 數據在 [`tables/legacy_all_experiment_metrics.csv`](../tables/legacy_all_experiment_metrics.csv)。

每個 version 最佳 baseline 在 [`tables/legacy_best_by_version.csv`](../tables/legacy_best_by_version.csv)。

## 局限

早期實驗未統一 holdout 切法、tension label 一度有誤、preprocessing 多次變動。
因此 v1-v6 數字**不適合直接跟 v17+ 比較**。

## 引用建議

可在 introduction / related work 提：「我們從 MobileNetV3 + TCN baseline 起步，
經過 v1-v10 的 fusion ablation 與 label 修正，轉向 ViT-based backbone（v15+）」。
