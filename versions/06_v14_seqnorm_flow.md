---
title: v14 SeqNorm
nav_order: 5
parent: 版本演進 (Version History)
---
# 06 — v14 Sequence Normalization + Flow Image 嘗試

## 動機

- v14: 加 sequence-level instance normalization
- v14a: CAXTON-style augmentation
- v14b: Sequence aug + full instance norm
- v14c: Sequence aug + image aug 組合

## 子封包

| 套件 | 主題 |
|---|---|
| v14_seqnorm_flowimage_package | sequence norm + flow image 變體 |
| v14a_caxton_augment_package | CAXTON augmentation |
| v14b_seqaug_fullinstanorm_package | seq augmentation + instance norm |
| v14c_seqaug_imgaug_package | seq aug + image aug 組合 |

## 全 run 表格

| package                           | run_id                                       | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:----------------------------------|:---------------------------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v14_seqnorm_flowimage_package     | v14_tcnonly_instanorm_seed1                  | scratch              | tcnonly         |                          0.6844 |                                    0.5222 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_aonly_moco_pretrained_seed2              | moco_pretrained      | aonly           |                          0.9529 |                                    0.5185 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_tcnonly_instanorm_seed3                  | scratch              | tcnonly         |                          0.7207 |                                    0.5154 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_tcnonly_instanorm_seed2                  | scratch              | tcnonly         |                          0.6752 |                                    0.5118 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_perheadgmu_moco_pretrained_seed1         | moco_pretrained      | perheadgmu      |                          0.9494 |                                    0.5050 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_conly_moco_pretrained_seed2              | moco_pretrained      | conly           |                          0.9471 |                                    0.4946 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_conly_moco_pretrained_seed3              | moco_pretrained      | conly           |                          0.9501 |                                    0.4818 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_gmu_moco_pretrained_include64train_seed2 | moco_pretrained      | gmu             |                          0.9425 |                                    0.4785 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_gmu_moco_pretrained_include64train_seed3 | moco_pretrained      | gmu             |                          0.9364 |                                    0.4721 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_perheadgmu_moco_pretrained_seed2         | moco_pretrained      | perheadgmu      |                          0.9234 |                                    0.4708 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_perheadgmu_moco_pretrained_seed3         | moco_pretrained      | perheadgmu      |                          0.9464 |                                    0.4692 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_conly_moco_pretrained_seed1              | moco_pretrained      | conly           |                          0.9475 |                                    0.4580 |                                                 nan |                                                nan |
| v14c_seqaug_imgaug_package        | v14c_seqaug_imgaug_seed1                     | moco_pretrained      | aonly           |                          0.9512 |                                    0.4576 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_aonly_moco_pretrained_seed3              | moco_pretrained      | aonly           |                          0.9437 |                                    0.4562 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_aonly_moco_pretrained_seed1              | moco_pretrained      | aonly           |                          0.9447 |                                    0.4485 |                                                 nan |                                                nan |
| v14a_caxton_augment_package       | v14a_caxton_augment_seed1                    | moco_pretrained      | caxton          |                          0.8533 |                                    0.4377 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_gmu_moco_pretrained_include64train_seed1 | moco_pretrained      | gmu             |                          0.9218 |                                    0.4304 |                                                 nan |                                                nan |
| v14b_seqaug_fullinstanorm_package | v14b_seqaug_fullinstanorm_seed1              | moco_pretrained      | gmu             |                          0.9522 |                                    0.4156 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_imgonly_moco_pretrained_seed1            | moco_pretrained      | imgonly         |                          0.9443 |                                    0.4002 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_imgonly_moco_pretrained_seed3            | moco_pretrained      | imgonly         |                          0.9384 |                                    0.3994 |                                                 nan |                                                nan |
| v14_seqnorm_flowimage_package     | v14_imgonly_moco_pretrained_seed2            | moco_pretrained      | imgonly         |                          0.9358 |                                    0.3942 |                                                 nan |                                                nan |

## 主要發現

- **Sequence instance norm 對 encoder-only 有幫助**（v14_tcnonly_instanorm 在 holdout flow 反而比 MobileNet+TCN 好）
- **Augmentation 提升有限**，無法解決 image encoder 對 flow 的根本不足
- v14 確認問題在 image encoder（不是 fusion 或 normalization）

## 為什麼這時期 plateau

整個 v11-v14 都用 MobileNetV3-Small backbone（為了部署考量）。flow head 的視覺信號需要更強的 backbone 才能學起來。
