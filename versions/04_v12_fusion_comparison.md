---
title: v12 Fusion 比較
nav_order: 3
parent: 版本演進 (Version History)
---

# v12 — Fusion Mechanism 大比較

## 動機

確定 image + encoder 雙模態必要後，對比不同 fusion 機制：

- **GMU** (Gated Multimodal Unit)
- **FiLM** (Feature-wise Linear Modulation)
- **Sum** (element-wise)
- **Concat** (128 / 256 變體)
- **Hadamard** (element-wise product)
- 加 CAXTON DKD warmup 變體

每個 fusion × scratch / CAXTON pretrained × 3 seeds ≈ 30 runs。

## 架構

- Image encoder: MobileNetV3-Small（frozen 或 CAXTON-adapted）
- TCN: 短 3-layer Conv1d
- Fusion: 變體
- 4 個 Linear heads（speed/flow/temp/tension）

## v12 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v12_hadamard_scratch_include64` | scratch | hadamard | 0.9095 | **0.4702** | — | — |
| `v12_hadamard_scratch_include64` | scratch | hadamard | 0.9257 | **0.4261** | — | — |
| `v12_concat_128_scratch_include` | scratch | concat_128 | 0.8905 | **0.4240** | — | — |
| `v12_concat_256_scratch_include` | scratch | concat_256 | 0.9058 | **0.4228** | — | — |
| `v12_gmu_scratch_include64train` | scratch | gmu | 0.8993 | **0.4028** | — | — |


## 主要發現

- **GMU 整體略勝**（id_val 略高，holdout 差距小）
- **FiLM 對某些頭較強**（v17 fusion swap 進一步驗證 FiLM 在 speed/flow 強）
- **CAXTON DKD warmup** 提升有限，但能避免訓練不穩
- **Fusion 選擇影響在 holdout 上小**（差距 < 0.05），瓶頸在 image encoder

## 衍生影響

v17 重做 fusion swap 進一步證實 ── 不同 fusion 在不同 head 強：

| Head | 最強 fusion |
|---|---|
| speed | FiLM |
| flow | FiLM |
| temp | Sum |
| tension | GMU（v17_orig）|

→ v24 採取 **per-head best fusion** 部署策略。
