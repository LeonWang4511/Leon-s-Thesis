---
title: ★ v24 部署優化
nav_order: 10
parent: 版本演進 (Version History)
---
# 11 — v24 Shallow Wide Package: 部署優化 + 多重 rescue

## 此章節地位

v24 是 thesis 的**集大成工程章節**。v17 之後的所有工作都在這個 package。

## 主要工作分類

### A. ViT-B 探索（capacity scaling）

| run | encoder | 結果（holdout avg4）|
|---|---|---:|
| v24_dinov2_vitb_5blk_seed1 | DINOv2 ViT-B/14 5blk | 0.524 |
| v24_dinov2_vitb_5blk_warmup15 | 同 + warmup15 | 0.473 |
| v24_dinov2_vitb_5blk_phase2 | Phase 2 | 0.487 |
| v24_dinov3_vitb_5blk_seed1 | DINOv3 ViT-B/16 5blk | 0.504 |

**結論**：ViT-B 比 ViT-S 差 0.05~0.15。tension 從 0.58 (ViT-S) 崩到 0.33 (ViT-B 全部變體)。**Shortcut learning 證據**（見 12 章）。

### B. SGD optimizer 探索

| run | optimizer | 結果 |
|---|---|---:|
| v17_5blk_sgd_pilot_seed1 | SGD momentum=0.9 lower lr | 0.581 |
| v17_5blk_sgd_pure_seed1 | SGD pure (lr=5e-2 head) | 0.580 |

SGD pure 略勝 AdamW (v17_5blk_seed1 = 0.551 raw)。

### C. Fusion swap (v17 5blk 架構下換 fusion)

| fusion | holdout avg4 (raw) | tension holdout | flow holdout |
|---|---:|---:|---:|
| GMU (baseline) | 0.580 | 0.525 | 0.601 |
| **FiLM** | 0.560 | **0.398** | **0.643** ← flow 強 |
| **Sum** | 0.567 | 0.434 | 0.629 |
| **Concat_256** | 0.561 | 0.434 | 0.612 |

GMU 整體最強，但 FiLM 在 flow / temp geom_ood 上強。

### D. SeqAux (給 TCN 加 tension 輔助 loss)

| run | tension holdout | 全 avg4 |
|---|---:|---:|
| v17_5blk_seqaux_sgd_seed1 | 0.59 | 0.589 |

TCN 加 aux loss 後 tension 邊際提升，但整體不顯著。

### E. Encoder ablation (詳見 12 章)

證明 temp param_ood 的失效是視覺信號根本不存在，不是 encoder shortcut。

### F. Rescue 嘗試（temp param_ood = 0.39 → 解不開）

| 嘗試 | 結果 |
|---|---|
| Class bias calibration | helpful，但只把 tension 從 0.58 → 0.79 |
| Per-head model 選最佳 | helpful，speed/flow 從 0.69 → 0.85 |
| Center crop TTA | 沒幫助 |
| Geo augmentation 重訓 | 反而傷 |
| Stacking with InceptionTime/MultiRocket | 沒幫助 |
| Adversarial 拔 speed/flow info | 全頭崩 |
| **Temp head retrain (color jitter heavy)** | **更差** |
| **Hotend sensor 輔助**（codex） | temp 達 1.000 但**已 ban**（非影像）|

### G. Causal smoothing (codex)

| rolling window | holdout tension | param_ood tension | geom_ood tension |
|---|---:|---:|---:|
| 5s | 0.733 | 0.807 | 0.652 |
| 20s | 0.788 | 0.868 | 0.702 |
| 50s | 0.822 | 0.894 | 0.745 |
| cumulative | 0.856 | 0.921 | 0.786 |

**rolling20s** 是當前 deployment 配置。

### H. Per-head best deployment（★ 最終配置）

| Head | Model | Bias [0, b1, b2] |
|---|---|---|
| speed | v17_5blk_film_sgd_seed1 | [0, +0.10, -0.55] |
| flow | v17_5blk_film_sgd_seed1 | [0, -0.05, -0.15] |
| temp | v17_5blk_sum_sgd_seed1 | [0, -0.05, -0.20] |
| tension | v17_5blk_seed1 (v17_orig) | [0, +0.75, +0.65] |

**結果（rolling20 deployment）**：

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.896 | 0.841 | 0.849 | 0.998 | 0.896 |
| id_test | 0.938 | 0.810 | 0.833 | 0.876 | 0.864 |
| internal_holdout | **0.905** | **0.851** | 0.540 | **0.789** | **0.771** |
| param_ood | **0.873** | **0.851** | 0.389 | **0.868** | 0.745 |
| geom_ood | **0.939** | **0.849** | 0.701 | **0.703** | **0.798** |

**11/12 head×subset cells ≥ 70%**，只有 temp holdout / temp param_ood 不過（結構性問題，見 12 章）。

### I. 嚴格 id_val-only 對比版本（沒 holdout leak）

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| internal_holdout | 0.905 | 0.773 | 0.516 | 0.382 | **0.644** |
| param_ood | 0.873 | 0.769 | 0.308 | 0.394 | 0.586 |
| geom_ood | 0.939 | 0.775 | 0.738 | 0.371 | 0.706 |

**差距**：嚴格 id_val 選法整體 avg4 約 0.64，比 holdout-informed 0.77 低 0.13。tension 大跌（v17_film 在 id_val 略高但在 holdout 崩）。

→ thesis 要老實標註「Version B 是 holdout-informed deployment selection」。

### J. ONNX 化（見 14 章）

PyTorch fp32 → ONNX fp16，accuracy 差 < 0.001。

## 全 run 表格

| package                  | run_id                                                 | image_encoder_init                           | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-------------------------|:-------------------------------------------------------|:---------------------------------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v24_shallow_wide_package | v17_5blk_seqaux_sgd_seed1                              | dinov3_truncated_5blk_seqaux                 | vit_dual        |                          0.7384 |                                    0.5892 |                                              0.5531 |                                             0.6252 |
| v24_shallow_wide_package | v24_tension_headonly_printbalanced_class3margin_seed1  | dinov3_truncated_5blk_seqaux                 | vit_dual        |                          0.7381 |                                    0.5878 |                                              0.5508 |                                             0.6242 |
| v24_shallow_wide_package | v24_tension_pcgrad_finetune_from_v17_seqaux_seed1      | dinov3_truncated_5blk_seqaux                 | vit_dual        |                          0.7449 |                                    0.5840 |                                              0.5513 |                                             0.6168 |
| v24_shallow_wide_package | v24_tension_ce_coral_aux_w0p2_seqaux_seed1             | dinov3_truncated_5blk_tension_ce_coral_aux   | vit_dual        |                          0.7395 |                                    0.5838 |                                              0.5453 |                                             0.6225 |
| v24_shallow_wide_package | v17_5blk_sgd_pilot_seed1                               | dinov3_truncated_5blk                        | vit_dual        |                          0.7335 |                                    0.5811 |                                              0.5562 |                                             0.6063 |
| v24_shallow_wide_package | v24_tension_rescue_printbalanced_class3margin_seed1    | dinov3_truncated_5blk_seqaux                 | vit_dual        |                          0.7122 |                                    0.5802 |                                              0.5378 |                                             0.6228 |
| v24_shallow_wide_package | v24_centercrop160_v17_5blk_seqaux_seed1                | dinov3_truncated_5blk_seqaux_center_crop_160 | vit_dual        |                          0.7303 |                                    0.5799 |                                              0.5553 |                                             0.6045 |
| v24_shallow_wide_package | v17_5blk_sgd_pure_seed1                                | dinov3_truncated_5blk                        | vit_dual        |                          0.7262 |                                    0.5799 |                                              0.5616 |                                             0.5974 |
| v24_shallow_wide_package | v24_v17best_headonly_pbmargin_seed1                    | dinov3_truncated_5blk                        | vit_dual        |                          0.6915 |                                    0.5689 |                                              0.5598 |                                             0.5766 |
| v24_shallow_wide_package | v24_geoaug_v17_5blk_seed1_fulltrain                    | dinov3_truncated_5blk                        | vit_dual        |                          0.6915 |                                    0.5688 |                                              0.5598 |                                             0.5764 |
| v24_shallow_wide_package | v24_v17best_branchb_fusionb_head_pbmargin_seed1        | dinov3_truncated_5blk                        | vit_dual        |                          0.6912 |                                    0.5673 |                                              0.5573 |                                             0.5758 |
| v24_shallow_wide_package | v24_v17best_geoaug_branchb_fusionb_head_pbmargin_seed1 | dinov3_truncated_5blk                        | vit_dual        |                          0.6911 |                                    0.5673 |                                              0.5573 |                                             0.5756 |
| v24_shallow_wide_package | v17_5blk_sum_sgd_seed1                                 | dinov3_truncated_5blk                        | vit_dual        |                          0.7478 |                                    0.5668 |                                              0.5316 |                                             0.6024 |
| v24_shallow_wide_package | v24_v17best_fusionb_head_pbmargin_seed1                | dinov3_truncated_5blk                        | vit_dual        |                          0.6908 |                                    0.5639 |                                              0.5551 |                                             0.5711 |
| v24_shallow_wide_package | v24_tension_ce_coral_aux_w0p5_seqaux_seed1             | dinov3_truncated_5blk_tension_ce_coral_aux   | vit_dual        |                          0.7412 |                                    0.5636 |                                              0.5203 |                                             0.6077 |
| v24_shallow_wide_package | v17_5blk_concat256_sgd_seed1                           | dinov3_truncated_5blk                        | vit_dual        |                          0.7586 |                                    0.5609 |                                              0.5204 |                                             0.6040 |
| v24_shallow_wide_package | v17_5blk_film_sgd_seed1                                | dinov3_truncated_5blk                        | vit_dual        |                          0.7557 |                                    0.5599 |                                              0.5178 |                                             0.6044 |
| v24_shallow_wide_package | v24_geoaug_v17_5blk_seed1_fulltrain_true               | dinov3_truncated_5blk                        | vit_dual        |                          0.6824 |                                    0.5440 |                                              0.5390 |                                             0.5480 |
| v24_shallow_wide_package | v24_dinov2_vits_5blk_sgd_pure_seed1                    | dinov2_vits_5blk                             | vit_dual        |                          0.7195 |                                    0.5387 |                                              0.5086 |                                             0.5687 |
| v24_shallow_wide_package | v24_dinov2_vitb_5blk_seed1                             | dinov2_vitb_5blk                             | vit_dual        |                          0.6942 |                                    0.5238 |                                              0.4867 |                                             0.5630 |
| v24_shallow_wide_package | v24_tension_coral_seqaux_seed1                         | dinov3_truncated_5blk_tension_coral          | vit_dual        |                          0.7364 |                                    0.5194 |                                              0.4821 |                                             0.5565 |
| v24_shallow_wide_package | v24_dinov3_vitb_5blk_seed1                             | dinov3_vitb_5blk                             | vit_dual        |                          0.6981 |                                    0.5041 |                                              0.4758 |                                             0.5335 |
| v24_shallow_wide_package | v24_dinov2_vitb_5blk_phase2_seed1                      | dinov2_vitb_5blk                             | vit_dual        |                          0.6289 |                                    0.4867 |                                              0.4513 |                                             0.5245 |
| v24_shallow_wide_package | v24_dinov2_vitb_5blk_warmup15_seed1                    | dinov2_vitb_5blk                             | vit_dual        |                          0.6339 |                                    0.4731 |                                              0.4367 |                                             0.5130 |
| v24_shallow_wide_package | v24_tension_only_v17_5blk_seqaux_seed1                 | dinov3_truncated_5blk_seqaux                 | vit_dual        |                          0.4661 |                                    0.3806 |                                              0.3852 |                                             0.3757 |


## v24 章節對 thesis 的價值

- 完整 **failure mode 證據**（為什麼 temp param_ood 解不了）
- 完整 **shortcut learning** 量化證據（capacity scaling）
- **per-head best + bias + smoothing** 部署方法論（可被引用）
- **ONNX 化路徑**驗證（部署可行）
