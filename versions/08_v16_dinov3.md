---
title: v16 DINOv3
nav_order: 7
parent: 版本演進 (Version History)
---
# 08 — v16 DINOv3 切換

## 動機

DINOv2 → DINOv3：DINOv3 是新版預訓練，對 OOD 圖像表現更穩定（Meta 2024）。

## 子封包

| 套件 | 主題 |
|---|---|
| v16_dinov3_package | DINOv3 ViT-S/16 完整版 + truncated 6blk |

## 全 run 表格

| package            | run_id                     | image_encoder_init    | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-------------------|:---------------------------|:----------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v16_dinov3_package | v16_lite_dinov3_6blk_seed1 | dinov3_truncated_6blk | vit_dual        |                          0.6589 |                                    0.6271 |                                              0.6037 |                                             0.6544 |
| v16_dinov3_package | v16_dinov3_seed1           | dinov3_dual           | vit_dual        |                          0.6108 |                                    0.6183 |                                              0.6030 |                                             0.6376 |
| v16_dinov3_package | v16_lite_mnv3_seed1        | mobilenetv3_lite      | gmu             |                          0.6329 |                                    0.5614 |                                              0.5379 |                                             0.5891 |
| v16_dinov3_package | v16_purevision_seed1       | dinov3_purevision     | none            |                          0.4963 |                                    0.3997 |                                              0.3965 |                                             0.4034 |

## 主要發現

- DINOv3 truncated 6blk 跟 DINOv2 full ViT-S 表現接近
- truncation 大幅減少參數但保留泛化能力
- → v17 進一步推到 5blk

## 為什麼 truncate 有效

DINOv3 ViT-S/16 共 12 blocks，但對小資料 fine-tuning 而言深層 blocks 反而 overfit。truncate 到 5-6 個 block 拿到 best trade-off。
