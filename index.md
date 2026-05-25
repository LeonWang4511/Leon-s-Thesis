---
title: Home
layout: home
nav_order: 0
---

<div style="text-align:center; padding: 2rem 1rem 2.5rem; background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%); border-radius: 12px; color: white; margin-bottom: 2rem;">

<h1 style="font-size: 2.6rem; font-weight: 800; margin-bottom: 0.5rem; color: white; -webkit-text-fill-color: white; background: none;">Leon's Thesis</h1>

<p style="font-size: 1.15rem; margin-bottom: 1.5rem; opacity: 0.95;">
FDM 3D 列印多模態監測 — 從 MobileNetV3 到 DINOv3 ViT 的完整研究歷程
</p>

<a href="00_INDEX" style="display:inline-block; background: white; color: #6d28d9 !important; padding: 0.7rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 0.3rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-bottom: none;">📖 開始閱讀</a>
<a href="12_shortcut_learning_diagnosis" style="display:inline-block; background: rgba(255,255,255,0.15); color: white !important; padding: 0.7rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 0.3rem; border: 1px solid rgba(255,255,255,0.3); border-bottom: 1px solid rgba(255,255,255,0.3);">★ 核心發現</a>
<a href="https://github.com/LeonWang4511/Leon-s-Thesis" style="display:inline-block; background: rgba(255,255,255,0.15); color: white !important; padding: 0.7rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 0.3rem; border: 1px solid rgba(255,255,255,0.3); border-bottom: 1px solid rgba(255,255,255,0.3);">⌥ GitHub</a>

</div>

## 🎯 核心研究發現

**DOE 設計缺陷誘發 ML Shortcut Learning** — 我們的 Taguchi L9(3³) 把 temp 設為 (speed × flow) 交互作用的線性函數。在 ML 訓練上，這直接轉化為模型走「(s, f) 視覺 → 查表」的捷徑，**從未學到真實溫度視覺信號**。Param-OOD holdout 上 temp 直接崩到 0.39（接近隨機）。

我們進一步證明 **inverse capacity scaling**：ViT-B (768-d) 比 ViT-S (384-d) 更糟，tension holdout 從 0.58 崩到 0.33。**更大模型不是學更好，而是更徹底走捷徑**。

[➜ 完整 Shortcut Learning 分析](12_shortcut_learning_diagnosis){: .btn .btn-purple }

---

## 📊 目前最佳成果

| 設定 | holdout avg4 |
|---|---:|
| MobileNet baseline (v13d) | 0.512 |
| v17 Canonical (DINOv3 ViT-S 5blk) | 0.652 |
| **★ Per-head best deployment** | **0.771** |

[➜ 全指標彙整](15_all_metrics_summary){: .btn .btn-purple }

---

## 🗺️ 演進時序

| 期間 | 版本 | 突破 | holdout avg4 |
|:---:|---|---|:---:|
| 2024–2025 | **v1–v10** | MobileNetV3 baseline 建立 | ~0.40 |
| 2025 | **v11–v14** | Fusion / Loss 迭代 | ~0.50 |
| 2025 | **v15–v16** | ⚡ DINOv2/v3 ViT 切換 | 0.65 |
| 2025–2026 | **v17** ★ | Truncated 5blk canonical | 0.65 |
| 2026 | **v18–v23** | Augmentation / Capacity | 0.75 |
| 2026 | **v24** ★ | Per-head best + shortcut 診斷 | **0.77** |

[➜ 完整版本演進](versions_index){: .btn .btn-purple }

---

## 🔗 快速導航

| 章節 | 內容 |
|---|---|
| [01 資料設計與 Taguchi L9](01_data_design) | 完整因子層次、切分、樣本數 |
| [09 v17 Canonical Model](versions/09_v17_canonical_5blk) | 當前 baseline 架構 |
| [11 v24 部署優化](versions/11_v24_shallow_wide) | Per-head best + bias + smoothing |
| [12 Shortcut Learning 診斷](12_shortcut_learning_diagnosis) | ★ 核心研究發現 |
| [13 TCN_v1 故障偵測](13_tcn_v1_fault_detector) | 第二個 model |
| [14 ONNX 部署](14_onnx_deployment) | fp16 量化 + RPi5 部署 |
| [15 全指標彙整](15_all_metrics_summary) | 179 runs 全部 metric |
| [16 經驗總結](16_lessons_learned) | Lessons + 未來方向 |

---

## 📦 資料規模

| 項目 | 數量 |
|---|---:|
| 訓練 prints | 57 |
| 訓練 images | 14,741 |
| 完整資料集 prints (1-99) | 99 |
| 完整資料集 windows | 28,455 |
| 故障 dataset prints (109-149) | 32 |
| 跑過的訓練實驗 (v11+) | 179 runs |
| 跑過的訓練實驗 (v1-v6 audit) | 358 runs |

---

<div style="text-align:center; padding: 1.5rem; color: #6b7280; font-size: 0.9rem;">
所有 .md 與 .csv 均為 <strong>UTF-8 with BOM</strong> 編碼。<br>
© 2026 LeonWang4511 — FDM Thesis Research History
</div>
