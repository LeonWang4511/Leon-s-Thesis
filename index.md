---
title: Home
layout: home
nav_order: 0
---

# Leon's Thesis 研究歷程
{: .fs-9 }

FDM 3D 列印多模態監測 — 從 MobileNetV3 baseline 到 DINOv3 ViT 部署的完整研究路徑
{: .fs-6 .fw-300 }

[開始閱讀（總導覽）](00_INDEX){: .btn .btn-purple .fs-5 .mb-4 .mb-md-0 .mr-2 }
[★ Shortcut Learning 診斷](12_shortcut_learning_diagnosis){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHub Repo](https://github.com/LeonWang4511/Leon-s-Thesis){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## 核心研究發現

**DOE 設計缺陷誘發 ML Shortcut Learning** — 我們的 Taguchi L9(3³) inner array 把 temp 設為 (speed × flow) 交互作用的線性函數。在 ML 訓練上，這直接轉化為模型走「(s, f) 視覺 → 查表」的捷徑，**從未學到真實溫度視覺信號**。Param-OOD holdout 上 temp 直接崩到 0.39（接近隨機）。

我們進一步證明 **inverse capacity scaling**：ViT-B (768-d) 比 ViT-S (384-d) 更糟，tension holdout 從 0.58 崩到 0.33。**更大模型不是學更好，而是更徹底走捷徑**。

[完整 shortcut learning 分析 →](12_shortcut_learning_diagnosis)

---

## 目前最佳成果

| 設定 | holdout avg4 |
|---|---:|
| MobileNet baseline (v13d) | 0.512 |
| v17 Canonical (DINOv3 ViT-S 5blk) | 0.652 |
| **★ Per-head best deployment** | **0.771** |

[全指標彙整 →](15_all_metrics_summary)

---

## 演進時序圖

```
2024-2025         2025                  2025-2026              2026
   │                │                       │                    │
   ▼                ▼                       ▼                    ▼
v1-v10           v11-v14                 v15-v16              v17-v24
MobileNetV3      Fusion / Loss           DINOv2/v3 ViT        Truncated 5blk
+ TCN            iteration               切換                 + 部署優化
                                                              + shortcut 診斷
holdout ~0.4    holdout ~0.5            holdout 0.65         holdout 0.77 (mix)
```

[完整版本演進 →](versions_index)

---

## 重點章節快速跳轉

- [01 資料設計與 Taguchi L9](01_data_design) — 完整的因子層次、切分方式、樣本數
- [09 v17 Canonical Model](versions/09_v17_canonical_5blk) — 當前 baseline 架構
- [11 v24 部署優化](versions/11_v24_shallow_wide) — Per-head best + bias + smoothing
- [12 Shortcut Learning 診斷](12_shortcut_learning_diagnosis) — 核心研究發現
- [13 TCN_v1 故障偵測](13_tcn_v1_fault_detector) — 第二個 model
- [14 ONNX 部署](14_onnx_deployment) — fp16 量化 + RPi5 部署
- [15 全指標彙整](15_all_metrics_summary) — 179 runs 全部 metric
- [16 經驗總結](16_lessons_learned) — Lessons + 未來方向

---

## 資料規模

| 項目 | 數量 |
|---|---:|
| 訓練 prints | 57 |
| 訓練 images | 14,741 |
| 完整資料集 prints (1-99) | 99 |
| 完整資料集 windows | 28,455 |
| 故障 dataset prints (109-149) | 32 |
| 跑過的訓練實驗 (v11+) | 179 runs |
| 跑過的訓練實驗 (v1-v6) | 358 runs |

---

## 編碼說明

本 repo 所有 `.md` 與 `.csv` 均為 **UTF-8 with BOM** 編碼，確保 Windows / Excel / 各 AI 工具都能正確讀取中文字符。

---

## License

個人 thesis 研究紀錄。引用前請聯繫作者。
