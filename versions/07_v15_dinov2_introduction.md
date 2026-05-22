---
title: v15 DINOv2 ViT 引入
nav_order: 6
parent: 版本演進 (Version History)
---

# v15 — DINOv2 ViT 切換 ⚡

## 動機

MobileNet 卡住。改用 self-supervised pretrained ViT (**DINOv2 ViT-S/14**) 試圖解決 flow head。

## 子封包

| 套件 | 主題 |
|---|---|
| `v15_dinov2_vit_package` | DINOv2 ViT-S baseline + mixup |
| `v15a_unfreeze_domadv_package` | Unfreeze + domain adversarial |
| `v15b_ablation_package` | Frozen / partial CAXTON adaptation |
| `v15c_dualenc_package` | ★ Dual encoder branch A/B |

## v15 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v15c_dualenc_seed1` | dinov2_dual | vit_dual | 0.7305 | **0.7863** | 0.7677 | 0.8083 |
| `v15c_dualenc_temporal_seed1` | dinov2_dual | vit_dual | 0.9133 | **0.6973** | 0.6802 | 0.7175 |
| `v15_dinov2_vit_seed1` | dinov2_pretrained | vit | 0.8528 | **0.5126** | — | — |
| `v15b_normonly_caxton_seed1` | dinov2_norm_only | vit | 0.8517 | **0.5020** | — | — |
| `v15_dinov2_vit_mixup_seed1` | dinov2_pretrained | vit_mixup | 0.7906 | **0.5017** | — | — |


## 重大突破：v15c dual-encoder

**v15c_dualenc** 把 ViT 分成兩個 branch：
- **Branch A** (frozen) → 給 speed/flow/temp
- **Branch B** (trainable) → 給 tension

| 指標 | 數值 |
|---|---:|
| holdout avg4 | **0.786** |
| 跟 MobileNet 時代差距 | **+0.27** |

證明 ViT backbone 是正確方向。

## 影響

**v17 直接繼承 v15c 的 dual-encoder 設計**，加上 truncation 進一步優化。
