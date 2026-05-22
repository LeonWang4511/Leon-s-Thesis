---
title: v18-v23 擴展
nav_order: 9
parent: 版本演進 (Version History)
---
# 10 — v18-v23 擴展嘗試

## 各擴展套件

| 套件 | 主題 | 結論 |
|---|---|---|
| v18_dinov2_augmentation_package | mixup / cutmix / geometric augment | mixup 在 holdout 0.719（中等改善）|
| v19_flow_targeted_aug_package | flow-targeted augmentation | F1 變體 holdout 0.670 |
| v20_arch_gradcam_study_package | 架構變體 + GradCAM 解釋 | 2-branch noseq 0.652 |
| v22_se_attention_package | SE attention 加成 | SE_cls 0.755 |
| v23_dinov2_vitl_ceiling_package | ViT-L (Large) 上限探索 | 容量過大反而 overfit |

## 全 run 表格

| package                         | run_id              | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:--------------------------------|:--------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v18_dinov2_augmentation_package | v18_mixup_seed1     | dinov2_dual          | vit_dual        |                          0.6867 |                                    0.7190 |                                              0.7194 |                                             0.7199 |
| v18_dinov2_augmentation_package | v18_cutmix_seed1    | dinov2_dual          | vit_dual        |                          0.6010 |                                    0.7054 |                                              0.6761 |                                             0.7401 |
| v18_dinov2_augmentation_package | v18_geometric_seed1 | dinov2_dual          | vit_dual        |                          0.5974 |                                    0.6914 |                                              0.6655 |                                             0.7218 |
| v18_dinov2_augmentation_package | v18_no_aug_seed1    | dinov2_dual          | vit_dual        |                          0.6848 |                                    0.6720 |                                              0.6808 |                                             0.6650 |

| package                       | run_id       | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:------------------------------|:-------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v19_flow_targeted_aug_package | v19_F1_seed1 | dinov2_dual          | vit_dual        |                          0.5910 |                                    0.6699 |                                              0.6549 |                                             0.6875 |

| package                        | run_id                  | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-------------------------------|:------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v20_arch_gradcam_study_package | v20_2branch_noseq_seed1 | dinov2_dual          | vit_dual        |                          0.5521 |                                    0.6518 |                                              0.6553 |                                             0.6453 |
| v20_arch_gradcam_study_package | v20_4branch_seq_seed1   | dinov2_dual          | vit_dual        |                          0.6437 |                                    0.5855 |                                              0.5426 |                                             0.6302 |
| v20_arch_gradcam_study_package | v20_1branch_seq_seed1   | dinov2_dual          | vit_dual        |                          0.6367 |                                    0.5483 |                                              0.5295 |                                             0.5690 |
| v20_arch_gradcam_study_package | v20_4branch_noseq_seed1 | dinov2_dual          | vit_dual        |                          0.5550 |                                    0.5367 |                                              0.4965 |                                             0.5797 |
| v20_arch_gradcam_study_package | v20_1branch_noseq_seed1 | dinov2_dual          | vit_dual        |                          0.5376 |                                    0.5259 |                                              0.4940 |                                             0.5602 |

| package                  | run_id           | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-------------------------|:-----------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v22_se_attention_package | v22_SE_cls_seed1 | dinov2_dual          | vit_dual        |                          0.6862 |                                    0.7547 |                                              0.7250 |                                             0.7898 |

| package                         | run_id                        | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:--------------------------------|:------------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v23_dinov2_vitl_ceiling_package | v23_dinov2_vitl_ceiling_seed1 | dinov2_vitl_dual     | vit_dual        |                          0.6244 |                                    0.5048 |                                              0.4804 |                                             0.5301 |


## 主要發現

1. **Augmentation 邊際效應遞減**：mixup ~0.72, geometric ~0.69，沒突破 v15c dualenc 的 0.78
2. **SE attention 略幫助**（v22 0.755）
3. **ViT-L 反而更差**（capacity scaling 揭示 shortcut learning，見 12 章）
4. **架構優化邊際**：2-branch / 4-branch 都沒明顯突破

## 影響

v18-v23 的探索讓我們意識到：
- 模型架構在這個資料規模下已經接近天花板
- 真正瓶頸在資料設計（L9 aliasing）和小樣本
- → 轉向 v24 的 deployment 優化 + shortcut learning 診斷
