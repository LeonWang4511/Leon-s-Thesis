---
title: ★ 全指標彙整
nav_order: 4
---
# 15 — 所有版本主指標彙整

## 來源

- 179 runs 從各 _package 目錄收集（v11+）
- 358 runs 從 experiment_metrics_audit（v1-v6）

## 各版本「最佳 holdout avg4」timeline

| 版本 | 最佳 run | encoder | fusion | holdout avg4 | param_ood | geom_ood |
|---|---|---|---|---:|---:|---:|
| v12_fusion_comparison_package          | v12_hadamard_scratch_include64train | scratch                   | hadamard   | 0.4702 | nan | nan |
| v13d_clean_data_package                | v13d_gmu_moco_pretrained_include64t | moco_pretrained           | gmu        | 0.5119 | nan | nan |
| v13_moco_fusion_package                | v13_gmu_moco_pretrained_include64tr | moco_pretrained           | gmu        | 0.4154 | nan | nan |
| v13c_domain_adversarial_package        | v13c_gmu_moco_pretrained_seed3      | moco_pretrained           | gmu        | 0.4120 | nan | nan |
| v14a_caxton_augment_package            | v14a_caxton_augment_seed1           | moco_pretrained           | caxton     | 0.4377 | nan | nan |
| v14b_seqaug_fullinstanorm_package      | v14b_seqaug_fullinstanorm_seed1     | moco_pretrained           | gmu        | 0.4156 | nan | nan |
| v14_seqnorm_flowimage_package          | v14_tcnonly_instanorm_seed1         | scratch                   | tcnonly    | 0.5222 | nan | nan |
| v14c_seqaug_imgaug_package             | v14c_seqaug_imgaug_seed1            | moco_pretrained           | aonly      | 0.4576 | nan | nan |
| v15a_unfreeze_domadv_package           | v15a_unfreeze_caxton_seed1          | dinov2_partial            | vit        | 0.4303 | nan | nan |
| v15c_dualenc_package                   | v15c_dualenc_seed1                  | dinov2_dual               | vit_dual   | 0.7863 | 0.7677 | 0.8083 |
| v15_dinov2_vit_package                 | v15_dinov2_vit_seed1                | dinov2_pretrained         | vit        | 0.5126 | nan | nan |
| v15b_ablation_package                  | v15b_normonly_caxton_seed1          | dinov2_norm_only          | vit        | 0.5020 | nan | nan |
| v16_dinov3_package                     | v16_lite_dinov3_6blk_seed1          | dinov3_truncated_6blk     | vit_dual   | 0.6271 | 0.6037 | 0.6544 |
| v17_caxton_adapted_package             | v17_6blk_seed2                      | dinov3_truncated_6blk     | vit_dual   | 0.7027 | 0.6806 | 0.7285 |
| v18_dinov2_augmentation_package        | v18_mixup_seed1                     | dinov2_dual               | vit_dual   | 0.7190 | 0.7194 | 0.7199 |
| v19_flow_targeted_aug_package          | v19_F1_seed1                        | dinov2_dual               | vit_dual   | 0.6699 | 0.6549 | 0.6875 |
| v20_arch_gradcam_study_package         | v20_2branch_noseq_seed1             | dinov2_dual               | vit_dual   | 0.6518 | 0.6553 | 0.6453 |
| v22_se_attention_package               | v22_SE_cls_seed1                    | dinov2_dual               | vit_dual   | 0.7547 | 0.7250 | 0.7898 |
| v23_dinov2_vitl_ceiling_package        | v23_dinov2_vitl_ceiling_seed1       | dinov2_vitl_dual          | vit_dual   | 0.5048 | 0.4804 | 0.5301 |
| v24_shallow_wide_package               | v17_5blk_seqaux_sgd_seed1           | dinov3_truncated_5blk_seq | vit_dual   | 0.5892 | 0.5531 | 0.6252 |


## Top 20 全期 holdout avg4

| Rank | run | package | encoder | holdout avg4 | param_ood | geom_ood |
|---:|---|---|---|---:|---:|---:|
| 1 | v15c_dualenc_seed1                       | v15c_dualenc_package      | dinov2_dual               | 0.7863 | 0.7677 | 0.8083 |
| 2 | v22_SE_cls_seed1                         | v22_se_attention_package  | dinov2_dual               | 0.7547 | 0.7250 | 0.7898 |
| 3 | v18_mixup_seed1                          | v18_dinov2_augmentation_p | dinov2_dual               | 0.7190 | 0.7194 | 0.7199 |
| 4 | v18_cutmix_seed1                         | v18_dinov2_augmentation_p | dinov2_dual               | 0.7054 | 0.6761 | 0.7401 |
| 5 | v17_6blk_seed2                           | v17_caxton_adapted_packag | dinov3_truncated_6blk     | 0.7027 | 0.6806 | 0.7285 |
| 6 | v15c_dualenc_temporal_seed1              | v15c_dualenc_package      | dinov2_dual               | 0.6973 | 0.6802 | 0.7175 |
| 7 | v18_geometric_seed1                      | v18_dinov2_augmentation_p | dinov2_dual               | 0.6914 | 0.6655 | 0.7218 |
| 8 | v17_6blk_seed3                           | v17_caxton_adapted_packag | dinov3_truncated_6blk     | 0.6893 | 0.6685 | 0.7132 |
| 9 | v18_no_aug_seed1                         | v18_dinov2_augmentation_p | dinov2_dual               | 0.6720 | 0.6808 | 0.6650 |
| 10 | v19_F1_seed1                             | v19_flow_targeted_aug_pac | dinov2_dual               | 0.6699 | 0.6549 | 0.6875 |
| 11 | v20_2branch_noseq_seed1                  | v20_arch_gradcam_study_pa | dinov2_dual               | 0.6518 | 0.6553 | 0.6453 |
| 12 | v16_lite_dinov3_6blk_seed1               | v16_dinov3_package        | dinov3_truncated_6blk     | 0.6271 | 0.6037 | 0.6544 |
| 13 | v16_dinov3_seed1                         | v16_dinov3_package        | dinov3_dual               | 0.6183 | 0.6030 | 0.6376 |
| 14 | v17_5blk_seqaux_sgd_seed1                | v24_shallow_wide_package  | dinov3_truncated_5blk_seq | 0.5892 | 0.5531 | 0.6252 |
| 15 | v24_tension_headonly_printbalanced_class | v24_shallow_wide_package  | dinov3_truncated_5blk_seq | 0.5878 | 0.5508 | 0.6242 |
| 16 | v20_4branch_seq_seed1                    | v20_arch_gradcam_study_pa | dinov2_dual               | 0.5855 | 0.5426 | 0.6302 |
| 17 | v24_tension_pcgrad_finetune_from_v17_seq | v24_shallow_wide_package  | dinov3_truncated_5blk_seq | 0.5840 | 0.5513 | 0.6168 |
| 18 | v24_tension_ce_coral_aux_w0p2_seqaux_see | v24_shallow_wide_package  | dinov3_truncated_5blk_ten | 0.5838 | 0.5453 | 0.6225 |
| 19 | v17_5blk_sgd_pilot_seed1                 | v24_shallow_wide_package  | dinov3_truncated_5blk     | 0.5811 | 0.5562 | 0.6063 |
| 20 | v24_tension_rescue_printbalanced_class3m | v24_shallow_wide_package  | dinov3_truncated_5blk_seq | 0.5802 | 0.5378 | 0.6228 |


## v17_orig per-frame raw metric (canonical 對照基準)

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.690 | 0.530 | 0.559 | 0.973 | 0.688 |
| id_test | 0.751 | 0.559 | 0.561 | 0.902 | 0.693 |
| internal_holdout | 0.684 | 0.495 | 0.444 | 0.582 | 0.551 |
| param_ood | 0.685 | 0.490 | 0.352 | 0.672 | 0.550 |
| geom_ood | 0.683 | 0.497 | 0.543 | 0.484 | 0.552 |

## v17_orig deployment metric (rolling20 + per-head bias)

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.808 | 0.643 | 0.748 | 0.998 | 0.799 |
| id_test | 0.910 | 0.631 | 0.725 | 0.876 | 0.785 |
| internal_holdout | 0.747 | 0.642 | 0.431 | 0.789 | 0.652 |
| param_ood | 0.757 | 0.650 | 0.295 | 0.868 | 0.643 |
| geom_ood | 0.742 | 0.630 | 0.580 | 0.703 | 0.663 |

## Per-head best mix deployment (Version B, ★ 最終)

詳見 11 章。

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| internal_holdout | 0.905 | 0.851 | 0.540 | 0.789 | **0.771** |
| param_ood | 0.873 | 0.851 | 0.389 | 0.868 | 0.745 |
| geom_ood | 0.939 | 0.849 | 0.701 | 0.703 | **0.798** |

## 嚴格 id_val-only deployment (Version A, no leak)

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| internal_holdout | 0.905 | 0.773 | 0.516 | 0.382 | 0.644 |
| param_ood | 0.873 | 0.769 | 0.308 | 0.394 | 0.586 |
| geom_ood | 0.939 | 0.775 | 0.738 | 0.371 | 0.706 |

## 完整原始 CSV

詳見 `tables/`：
- `all_metrics_master.csv` — 179 runs 所有 subset 所有 head 完整指標
- `all_runs_index.csv` — 簡表，每 run 核心指標
- `best_per_package.csv` — 每套件最佳 run
- `legacy_*.csv` — v1-v6 era 358 筆
