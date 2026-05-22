---
title: v12 Fusion 比較
nav_order: 3
parent: 版本演進 (Version History)
---
# 04 — v12 Fusion Comparison

## 動機

確定 image + encoder 雙模態必要後，對比不同 fusion 機制：
- GMU (Gated Multimodal Unit)
- FiLM (Feature-wise Linear Modulation)
- Sum (element-wise sum)
- Concat (128, 256 變體)
- Hadamard (element-wise product)
- 加 CAXTON DKD warmup 變體

每個 fusion × scratch / CAXTON pretrained × 3 seeds = ~30 runs。

## 架構

- Image encoder: MobileNetV3-Small (frozen 或 CAXTON-adapted)
- TCN: 短 3-layer conv1d
- Fusion: 上述各種
- 4 個 Linear heads

## 全 run 表格

| package                       | run_id                                         | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:------------------------------|:-----------------------------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v12_fusion_comparison_package | v12_hadamard_scratch_include64train_seed1      | scratch              | hadamard        |                          0.9095 |                                    0.4702 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_hadamard_scratch_include64train_seed2      | scratch              | hadamard        |                          0.9257 |                                    0.4261 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_128_scratch_include64train_seed3    | scratch              | concat_128      |                          0.8905 |                                    0.4240 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_256_scratch_include64train_seed3    | scratch              | concat_256      |                          0.9058 |                                    0.4228 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_scratch_include64train_seed3           | scratch              | gmu             |                          0.8993 |                                    0.4028 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_hadamard_scratch_include64train_seed3      | scratch              | hadamard        |                          0.8988 |                                    0.3956 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_256_scratch_include64train_seed2    | scratch              | concat_256      |                          0.9141 |                                    0.3952 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_128_scratch_include64train_seed1    | scratch              | concat_128      |                          0.8993 |                                    0.3947 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_scratch_include64train_seed2           | scratch              | gmu             |                          0.9178 |                                    0.3929 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_scratch_include64train_seed1           | scratch              | sum             |                          0.8923 |                                    0.3921 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_256_scratch_include64train_seed1    | scratch              | concat_256      |                          0.8984 |                                    0.3900 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_film_scratch_include64train_seed1          | scratch              | film            |                          0.9055 |                                    0.3784 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_scratch_include64train_seed1           | scratch              | gmu             |                          0.9118 |                                    0.3760 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_caxton_dkd_warmup_include64train_seed1 | caxton_dkd_warmup    | gmu             |                          0.9251 |                                    0.3729 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_scratch_include64train_seed3           | scratch              | sum             |                          0.8695 |                                    0.3721 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_concat_128_scratch_include64train_seed2    | scratch              | concat_128      |                          0.9201 |                                    0.3621 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_caxton_dkd_warmup_include64train_seed3 | caxton_dkd_warmup    | sum             |                          0.8830 |                                    0.3575 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_film_scratch_include64train_seed3          | scratch              | film            |                          0.9052 |                                    0.3571 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_caxton_dkd_warmup_include64train_seed2 | caxton_dkd_warmup    | gmu             |                          0.9017 |                                    0.3461 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_caxton_dkd_warmup_include64train_seed2 | caxton_dkd_warmup    | sum             |                          0.9242 |                                    0.3435 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_gmu_caxton_dkd_warmup_include64train_seed3 | caxton_dkd_warmup    | gmu             |                          0.9207 |                                    0.3434 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_film_scratch_include64train_seed2          | scratch              | film            |                          0.9265 |                                    0.3369 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_scratch_include64train_seed2           | scratch              | sum             |                          0.8877 |                                    0.3317 |                                                 nan |                                                nan |
| v12_fusion_comparison_package | v12_sum_caxton_dkd_warmup_include64train_seed1 | caxton_dkd_warmup    | sum             |                          0.9021 |                                    0.2993 |                                                 nan |                                                nan |

## 主要發現

- **GMU 整體略勝**（id_val 高但 holdout 跟其他差距小）
- **FiLM 對某些頭較強**（後在 v17 fusion swap 驗證 FiLM 在 speed/flow 強）
- **CAXTON DKD warmup** 提升有限，但能避免訓練不穩
- **fusion 選擇影響在 holdout 上很小**（差距 < 0.05），主要瓶頸是 image encoder 而非 fusion

## 啟示

v17 5blk 時期重做 fusion swap 進一步證實：
- v17_film 在 speed/flow holdout 反而比 v17_orig (GMU) 強
- 但 v17_film 在 tension holdout 崩到 0.38
- → 沒有單一 fusion 是全頭最佳

## 衍生影響

v24_shallow_wide 採取 **per-head best fusion** 策略：speed/flow 用 v17_film, temp 用 v17_sum, tension 用 v17_orig（見 11 章）。
