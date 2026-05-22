---
title: v13 MoCo + Clean Data
nav_order: 4
parent: 版本演進 (Version History)
---

# v13 — MoCo Pretraining + Clean Data 系列

## 動機

- v13: 加入 MoCo self-supervised pretraining
- v13c: 加 domain adversarial
- **v13d: 清洗訓練資料、修正錯誤標籤、最終 MobileNet baseline**
- v13e: 純 image-only 對照

## 子封包

| 套件 | 主題 |
|---|---|
| `v13_moco_fusion_package` | MoCo pretrained + GMU/Sum |
| `v13a_gradcam_diagnosis` | GradCAM 視覺解釋 |
| `v13b_caxton_l27_image_only_runs` | CAXTON L27 + image only |
| `v13c_domain_adversarial_package` | Domain adversarial training |
| `v13d_clean_data_package` | ★ 最終乾淨資料 baseline |
| `v13e_imgonly_comparison_package` | Image-only 對照 |

## v13 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v13d_gmu_moco_pretrained_inclu` | moco_pretrained | gmu | 0.9411 | **0.5119** | — | — |
| `v13d_gmu_moco_pretrained_inclu` | moco_pretrained | gmu | 0.9537 | **0.5086** | — | — |
| `v13d_gmu_moco_pretrained_inclu` | moco_pretrained | gmu | 0.9346 | **0.4554** | — | — |
| `v13_gmu_moco_pretrained_includ` | moco_pretrained | gmu | 0.9144 | **0.4154** | — | — |
| `v13c_gmu_moco_pretrained_seed3` | moco_pretrained | gmu | 0.9268 | **0.4120** | — | — |


## v13d — MobileNet 時代最佳 baseline

**MobileNetV3 + MoCo + GMU**:

| 指標 | 數值 |
|---|---:|
| id_val avg4 | 0.93 ~ 0.95 |
| holdout avg4 (best seed) | **0.51** |
| holdout flow | **≈ 0.01** ← 完全不會泛化 |
| holdout tension | ≈ 0.95 |

## 主要限制

- **Flow head 在 holdout 完全失效** (balanced acc ≈ 0)
- MobileNet image encoder 無法區分視覺接近的 flow 90 / 100 / 110

## 結論

需要更強的 image encoder → **v15 切換到 DINOv2 ViT 是直接後果**。
