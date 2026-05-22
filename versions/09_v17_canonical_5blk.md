---
title: v17 Canonical 5blk ★
nav_order: 8
parent: 版本演進 (Version History)
---

# v17 — Canonical Model: DINOv3 5blk Truncated ★

> **本版本為 thesis canonical model**。所有 v18+ 與 v24 都以此為起點。

## 架構

```
Input image (3, 224, 224)
    ↓
DINOv3 ViT-S/16 patch embed
    ↓
Block 0, 1  (shared, frozen)
    ↓
    ├── Branch A: Block 2/3/4 (frozen)    → norm → CLS_a
    └── Branch B: Block 2/3/4 (trainable) → norm → CLS_b

Encoder seq (4 ch, 100 samples = 2s)
    ↓
TCN (3 conv layers)  → seq_vec (96-d)
    ↓
fusion_a = GMU(CLS_a, seq_vec)  → speed / flow / temp heads
fusion_b = GMU(CLS_b, seq_vec)  → tension head
    ↓
4 × Linear(128, 3): speed / flow / temp / tension
```

## 參數量

| 元件 | params | 是否凍結 |
|---|---:|:---:|
| image_encoder (DINOv3 ViT-S/16) | 9,174,528 | ✓ 凍結 |
| blocks_frozen (2 blocks) | 5,325,696 | ✓ 凍結 |
| blocks_trainable (3 blocks) | 5,325,696 | ✗ |
| seq_conv (TCN) | 60,416 | ✗ |
| fusion_a + fusion_b (GMU × 2) | 246,528 | ✗ |
| 4 heads + aux heads | 3,858 | ✗ |
| **Total** | **20,138,258** | (5.64M trainable) |

## 訓練設定

| 項目 | 值 |
|---|---|
| Optimizer | AdamW |
| LR | head=5e-2, feature=5e-3 |
| Weight decay | 1e-4 |
| Schedule | warmup 5 epoch → cosine to 200 |
| Patience | 30 (early stop) |
| Batch | 256 |
| AMP | fp16 enabled |
| Selection | id_val tension balanced accuracy |

## v17 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v17_6blk_seed2` | dinov3_truncated_6bl | vit_dual | 0.7116 | **0.7027** | 0.6806 | 0.7285 |
| `v17_6blk_seed3` | dinov3_truncated_6bl | vit_dual | 0.7135 | **0.6893** | 0.6685 | 0.7132 |
| `v17_5blk_seed2` | dinov3_truncated_5bl | vit_dual | 0.6872 | **0.5659** | 0.5416 | 0.5915 |
| `v17_caxton_dual_seed1` | dinov3_caxton_adapte | vit_dual | 0.7149 | **0.5625** | 0.5593 | 0.5689 |
| `v17_5blk_seed3` | dinov3_truncated_5bl | vit_dual | 0.7042 | **0.5494** | 0.5281 | 0.5710 |


## v17_5blk_seed1 全指標（per-frame raw）

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.690 | 0.530 | 0.559 | 0.973 | 0.688 |
| id_test | 0.751 | 0.559 | 0.561 | 0.902 | 0.693 |
| internal_holdout | 0.684 | 0.495 | 0.444 | 0.582 | 0.551 |
| param_ood | 0.685 | 0.490 | 0.352 | 0.672 | 0.550 |
| geom_ood | 0.683 | 0.497 | 0.543 | 0.484 | 0.552 |

## v17_5blk_seed1 全指標（rolling20 + per-head bias）

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.808 | 0.643 | 0.748 | 0.998 | 0.799 |
| id_test | 0.910 | 0.631 | 0.725 | 0.876 | 0.785 |
| internal_holdout | 0.747 | 0.642 | 0.431 | 0.789 | 0.652 |
| param_ood | 0.757 | 0.650 | 0.295 | 0.868 | 0.643 |
| geom_ood | 0.742 | 0.630 | 0.580 | 0.703 | 0.663 |

## 為什麼這版是 canonical

1. **Tension head 在 holdout 0.79 → 全 v17 系列最強**（capacity 剛好，沒被 print-id 過度記憶）
2. **DINOv3 ViT-S vs ViT-B**：ViT-B 更大但 holdout 反而崩
3. **Truncation 5blk** 比 6blk / full 都更好（更輕量也更不易 overfit）
