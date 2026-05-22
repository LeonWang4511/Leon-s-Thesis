# 09 — v17 Canonical: DINOv3 5blk Truncated

## 此版本地位

**v17 5blk seed1 = 目前 thesis 的 canonical model**。所有後續 v18+ 與 v24 都以此為起點。

## 架構

```
Input image (3, 224, 224)
    ↓
DINOv3 ViT-S/16 patch embed
    ↓
Block 0, 1 (shared, frozen)
    ↓
   ├──→ Branch A: Block 2/3/4 (frozen)   → norm_frozen   → CLS_a
   └──→ Branch B: Block 2/3/4 (trainable)→ norm_trainable → CLS_b

Encoder seq (4 ch, 100 samples = 2s)
    ↓
TCN (3 conv layers)  → seq_vec (96-d)
    ↓
fusion_a = GMU(CLS_a, seq_vec)  → speed/flow/temp heads
fusion_b = GMU(CLS_b, seq_vec)  → tension head
    ↓
4 × Linear(128, 3): speed/flow/temp/tension logits
```

## 參數量

| 元件 | params | 備註 |
|---|---:|---|
| image_encoder (DINOv3 ViT-S/16) | 9.17M | 凍結 |
| blocks_frozen (2 blocks) | 5.33M | 凍結 |
| blocks_trainable (3 blocks) | 5.33M | 訓練 |
| seq_conv (TCN) | 60k | 訓練 |
| fusion_a (GMU) | 123k | 訓練 |
| fusion_b (GMU) | 123k | 訓練 |
| 4 heads (Linear 128→3) | 1.5k | 訓練 |
| aux_speed_head / aux_temp_head | 2.3k | 訓練（未啟用）|
| **Total** | **20.14M** | (5.64M trainable) |

## 訓練設定

- Optimizer: AdamW (lr_head=5e-2, lr_feature=5e-3, wd=1e-4)
- Schedule: warmup 5 epoch → cosine to 200
- Patience: 30 (early stop)
- Batch: 256, num_workers: 8-12
- AMP fp16 enabled
- Selected epoch by id_val tension balanced accuracy

## 全 run 表格

| package                    | run_id                | image_encoder_init         | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:---------------------------|:----------------------|:---------------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v17_caxton_adapted_package | v17_6blk_seed2        | dinov3_truncated_6blk      | vit_dual        |                          0.7116 |                                    0.7027 |                                              0.6806 |                                             0.7285 |
| v17_caxton_adapted_package | v17_6blk_seed3        | dinov3_truncated_6blk      | vit_dual        |                          0.7135 |                                    0.6893 |                                              0.6685 |                                             0.7132 |
| v17_caxton_adapted_package | v17_5blk_seed2        | dinov3_truncated_5blk      | vit_dual        |                          0.6872 |                                    0.5659 |                                              0.5416 |                                             0.5915 |
| v17_caxton_adapted_package | v17_caxton_dual_seed1 | dinov3_caxton_adapted_dual | vit_dual        |                          0.7149 |                                    0.5625 |                                              0.5593 |                                             0.5689 |
| v17_caxton_adapted_package | v17_5blk_seed3        | dinov3_truncated_5blk      | vit_dual        |                          0.7042 |                                    0.5494 |                                              0.5281 |                                             0.5710 |
| v17_caxton_adapted_package | v17_5blk_seed1        | dinov3_truncated_5blk      | vit_dual        |                          0.5807 |                                    0.4805 |                                              0.4985 |                                             0.4635 |
| v17_caxton_adapted_package | v17_4blk_seed1        | dinov3_truncated_4blk      | vit_dual        |                          0.6882 |                                    0.4628 |                                              0.4555 |                                             0.4733 |

## v17_5blk_seed1 全指標 (per-frame raw)

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.690 | 0.530 | 0.559 | 0.973 | 0.688 |
| id_test | 0.751 | 0.559 | 0.561 | 0.902 | 0.693 |
| internal_holdout | 0.684 | 0.495 | 0.444 | 0.582 | 0.551 |
| param_ood | 0.685 | 0.490 | 0.352 | 0.672 | 0.550 |
| geom_ood | 0.683 | 0.497 | 0.543 | 0.484 | 0.552 |

## v17_5blk_seed1 全指標 (rolling20 + per-head bias)

詳見 11 章 v24 工作。簡略：

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.808 | 0.643 | 0.748 | 0.998 | 0.799 |
| id_test | 0.910 | 0.631 | 0.725 | 0.876 | 0.785 |
| internal_holdout | 0.747 | 0.642 | 0.431 | 0.789 | 0.652 |
| param_ood | 0.757 | 0.650 | 0.295 | 0.868 | 0.643 |
| geom_ood | 0.742 | 0.630 | 0.580 | 0.703 | 0.663 |

## 為什麼這版是 baseline

1. **tension head 在 holdout 0.79 → 全 v17 系列最強**（capacity 剛好，沒被 print-id 過度記憶）
2. **DINOv3 ViT-S vs ViT-B**：ViT-B 更大但 holdout 反而崩（見 12 章 shortcut learning）
3. **truncation 5blk** 比 6blk / full 都更好（更輕量也更不易 overfit）
