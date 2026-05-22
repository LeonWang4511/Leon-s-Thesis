---
title: v24 部署優化 ★
nav_order: 10
parent: 版本演進 (Version History)
---

# v24 — Shallow Wide Package: 部署優化 + 多重 Rescue ★

> 本章節是 thesis 的**集大成工程章節**。v17 之後的所有工作都在這個 package。

## v24 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v17_5blk_seqaux_sgd_seed1` | dinov3_truncated_5bl | vit_dual | 0.7384 | **0.5892** | 0.5531 | 0.6252 |
| `v24_tension_headonly_printbala` | dinov3_truncated_5bl | vit_dual | 0.7381 | **0.5878** | 0.5508 | 0.6242 |
| `v24_tension_pcgrad_finetune_fr` | dinov3_truncated_5bl | vit_dual | 0.7449 | **0.5840** | 0.5513 | 0.6168 |
| `v24_tension_ce_coral_aux_w0p2_` | dinov3_truncated_5bl | vit_dual | 0.7395 | **0.5838** | 0.5453 | 0.6225 |
| `v17_5blk_sgd_pilot_seed1` | dinov3_truncated_5bl | vit_dual | 0.7335 | **0.5811** | 0.5562 | 0.6063 |


## 主要工作分類

### A. ViT-B 容量探索（capacity scaling 證據）

| Run | Encoder | Holdout avg4 |
|---|---|---:|
| `v24_dinov2_vitb_5blk` | DINOv2 ViT-B/14 5blk | 0.524 |
| `v24_dinov2_vitb_5blk_warmup15` | + warmup15 | 0.473 |
| `v24_dinov2_vitb_5blk_phase2` | Phase 2 | 0.487 |
| `v24_dinov3_vitb_5blk` | DINOv3 ViT-B/16 5blk | 0.504 |

**結論**：ViT-B 比 ViT-S 差 0.05-0.15。Tension 從 0.58 (ViT-S) 崩到 **0.33** (ViT-B 全部變體)。
→ Shortcut learning 證據（詳見 [Shortcut Learning 診斷](../12_shortcut_learning_diagnosis)）。

### B. Fusion Swap（換 fusion）

| Fusion | Holdout avg4 | tension | flow |
|---|---:|---:|---:|
| GMU (baseline) | 0.580 | 0.525 | 0.601 |
| **FiLM** | 0.560 | 0.398 | **0.643** ← flow 強 |
| **Sum** | 0.567 | 0.434 | 0.629 |
| **Concat_256** | 0.561 | 0.434 | 0.612 |

GMU 整體最強，但 FiLM 在 flow / temp geom_ood 上強。

### C. SGD vs AdamW

| Run | Holdout avg4 |
|---|---:|
| `v17_5blk_sgd_pure_seed1` | 0.580 |
| `v17_5blk_seed1` (AdamW) | 0.551 |

SGD pure 略勝 AdamW。

### D. Rescue 嘗試（全失敗，**temp param_ood 解不開**）

| 嘗試 | 結果 |
|---|---|
| Class bias calibration | helpful，tension 0.58 → 0.79 |
| Per-head best model 選最佳 | helpful，speed/flow 0.69 → 0.85 |
| Center crop TTA | ❌ |
| Geo augmentation 重訓 | ❌ 反而傷 |
| Stacking with InceptionTime/MultiRocket | ❌ |
| Adversarial 拔 speed/flow info | ❌ 全頭崩 |
| Temp head retrain (heavy color jitter) | ❌ 更差 |

### E. Causal Smoothing

| Rolling Window | holdout tension | param_ood | geom_ood |
|---|---:|---:|---:|
| 5s | 0.733 | 0.807 | 0.652 |
| **20s** | **0.788** | **0.868** | **0.702** |
| 50s | 0.822 | 0.894 | 0.745 |
| cumulative | 0.856 | 0.921 | 0.786 |

**rolling20s** 是當前 deployment 配置（trade-off：延遲 vs 準度）。

### F. Per-Head Best Deployment ★

| Head | Model | Bias [0, b1, b2] |
|---|---|---|
| speed | `v17_5blk_film_sgd_seed1` | [0, +0.10, -0.55] |
| flow | `v17_5blk_film_sgd_seed1` | [0, -0.05, -0.15] |
| temp | `v17_5blk_sum_sgd_seed1` | [0, -0.05, -0.20] |
| tension | `v17_5blk_seed1` (v17_orig) | [0, +0.75, +0.65] |

**Per-head best 全指標（rolling20 deployment）**：

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.896 | 0.841 | 0.849 | 0.998 | 0.896 |
| id_test | 0.938 | 0.810 | 0.833 | 0.876 | 0.864 |
| **internal_holdout** | **0.905** | **0.851** | 0.540 | **0.789** | **0.771** |
| **param_ood** | **0.873** | **0.851** | 0.389 | **0.868** | 0.745 |
| **geom_ood** | **0.939** | **0.849** | 0.701 | **0.703** | **0.798** |

✓ **11 / 12 head × subset cells ≥ 70%**

✗ Temp holdout (0.540) 與 temp param_ood (0.389) 是結構性 aliasing 問題
   （詳見 [Shortcut Learning 診斷](../12_shortcut_learning_diagnosis)）

### G. 嚴格 id_val-only 對比（無 holdout leak）

| Subset | avg4 |
|---|---:|
| internal_holdout | 0.644 |
| param_ood | 0.586 |
| geom_ood | 0.706 |

差距：嚴格 id_val 比 holdout-informed 低 ~0.13。Thesis 要老實標註。

### H. ONNX 化（見 [ONNX 部署](../14_onnx_deployment)）

PyTorch fp32 → ONNX fp16：accuracy 差 < 0.001，檔案省 62%。

## 對 thesis 的價值

- 完整 **failure mode 證據**（為什麼 temp param_ood 解不了）
- 完整 **shortcut learning** 量化證據（capacity scaling）
- **per-head best + bias + smoothing** 部署方法論
- **ONNX 化路徑**驗證（部署可行）
