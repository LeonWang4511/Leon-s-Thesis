# 16 — 經驗總結 + 未來方向

## 核心經驗（成功）

### 1. 小樣本 ML 訓練資料設計的盲點

傳統 DOE 教科書推薦的 L9 / L18 等小型正交陣，**在 ML 訓練上可能誘發 shortcut learning**。具體：
- L9(3³) inner array 把 temp 設為 (s × f) interaction → ML 走捷徑
- L27(3¹³) 4-factor placement at C1/C2/C5/C9 → 無此問題

**這個 framing 是 thesis 主要 contribution**。

### 2. Capacity scaling 並非萬靈丹

ViT-S → ViT-B 容量翻倍，**holdout 表現反而下降**：
- ViT-S tension holdout: 0.58
- ViT-B tension holdout: 0.33（隨機）

→ 在 aliased 訓練資料下，**capacity 越大越被誘往 shortcut**。

### 3. Per-head best mix > 單一 model

不同 head 在不同 fusion 上表現不同：
- speed/flow: FiLM 強
- temp: Sum 強
- tension: GMU (v17_orig) 強

組合起來比單一 model 提升 +0.12 avg4。但要老實標註 holdout-informed selection。

### 4. Rolling smoothing 是廉價的部署優化

對 print-level 靜態因子（speed/flow/temp/tension 都是設定），rolling20s 後處理把 tension 從 0.58 → 0.79。**不需要重訓**。

### 5. ONNX 化幾乎無痛

- fp16 量化：accuracy 差 < 0.001
- 檔案省 62%
- RPi5 推論加速 2-3 倍

## 核心經驗（失敗）

### A. Temp param_ood 是結構性死路

所有嘗試（augmentation、retrain、TTA、stacking、ensemble、adversarial）都救不了 temp param_ood。原因：訓練資料根本不要求模型學溫度視覺。

**只有改資料設計（L27）能解。**

### B. ViT-B / ViT-L 不適合此 dataset

容量過大誘發 shortcut。在小樣本（< 20k）上，**較小 backbone (ViT-S 5blk truncated) 反而泛化更好**。

### C. Hyperparameter sweep 邊際遞減

v18-v23 的 augmentation / attention / architecture variation 都沒突破 v15c dualenc 的 0.78 holdout avg4。

### D. Codex 的 hotend sensor「救援」不算數

用 hotend telemetry 直接量測（非影像）讓 temp 達 1.000，但這違反「pure image+encoder」研究目標。已 ban。

## 部署落地（已完成）

- v17_orig (ONNX fp16, 29 MB) + TCN_v1 (3.5 MB) = **~33 MB** 部署套件
- RPi5 + ONNX Runtime CPU EP，預估 3-4 FPS
- Per-head best mix deployment config (Version B) 已凍結

## 未來方向（依優先序）

### 1. ★ L27(3¹³) 重訓 — thesis paper 1 主要 future work

具體計畫：
- 27 個唯一 (s, f, t, tension) × 3 pieces = **54 個新印件**（9 既有可重用 × 3 = 27 + 54 = 81 total）
- 用 standard Taguchi L27 + linear graph 規範（C1=speed, C2=flow, C5=temp, C9=tension）
- 重訓 v17_5blk + 任何 backbone
- 預期：temp param_ood 從 0.39 → 0.65+

### 2. ☆ 27 件 counter-example patch — 較省方案

不重做整個設計，加 27 個破 L9 的印件 + 訓練時 oversample × 3。實際印件量：~27 件新。詳見 11 章「Option C」討論。

### 3. TCN_v1 重新 evaluation 並 ONNX 化

目前 TCN_v1 checkpoint 沒存 val/test metrics。需要：
- 重跑 evaluation 量出 5-class accuracy
- Export ONNX fp16
- 整合 deployment aggregator script

### 4. 寫 deployment aggregator

把 v17 ONNX 輸出 + TCN_v1 ONNX 輸出 + state machine 整合成單一 service。預估 ~200 行 Python。

### 5. 真實場域驗證

挑 9 個訓練分布內的高 F1 print（已選好）重印一次，驗證 deployment 可重現性。
詳見之前討論的「9 個驗證 print」清單。

### 6. Paper 1: DOE × ML shortcut methodology

- Title: "Orthogonal Design Aliasing as Source of Shortcut Learning"
- Target: IISE Transactions / Quality Engineering / J. Manufacturing Systems
- 主要 data: 此 thesis 的 L9 vs L27 對比 + capacity scaling
- 投稿時間：L27 重訓完成後

### 7. Paper 2: FDM 多模態監測系統

- Title: "Multi-Modal Monitoring System for FDM Quality Control with Aliasing-Aware Data Design"
- Target: Additive Manufacturing / J. Manufacturing Processes
- 主要 data: per-head best deployment + ONNX + RPi5 部署
- 引用 Paper 1 的 methodology

## 核心訊息（給未來自己）

1. **資料設計 > 模型架構**（小樣本領域特別明顯）
2. **越大模型不等於越好**（aliasing 下反而更壞）
3. **deployment-level optimization 廉價有效**（per-head + bias + smoothing）
4. **誠實標註 holdout-informed 部分**（research 倫理）
5. **DOE × ML 是真正的 research gap**（少有人探索）

## Repo 索引

| Path | 重要內容 |
|---|---|
| `v17_caxton_adapted_package/runs/v17_results/v17_5blk_seed1/` | canonical model checkpoint |
| `v24_shallow_wide_package/runs/v24_final_deployment/` | per-head best deployment config |
| `v24_shallow_wide_package/runs/v24_onnx_export/` | ONNX fp32/fp16 + 比對 metric |
| `v24_shallow_wide_package/runs/v24_all_heads_calibration/` | per-head logit + bias calibration |
| `v24_shallow_wide_package/runs/v24_all_heads_rescue_codex/` | codex 的多重 rescue 嘗試 |
| `.claude/worktrees/peaceful-volhard-fc16f8/` | TCN_v1 fault detector |
| `experiment_metrics_audit/` | v1-v6 era 358 runs audit |
| `RESEARCH_HISTORY/` | 本資料夾（完整歷程整理）|

## 致謝

- Claude / Codex 協助迭代與分析
- 大量 failure modes 被誠實記錄而非掩蓋，是論文 honest contribution 的基礎
