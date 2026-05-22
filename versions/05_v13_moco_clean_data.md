# 05 — v13 MoCo Pretraining + Clean Data 系列

## 動機

1. 加入 MoCo self-supervised pretraining（v13）
2. 比較 scratch vs MoCo
3. v13c 加 domain adversarial
4. **v13d**：清洗訓練資料、修正錯誤標籤、最終 baseline
5. v13e：純 image-only 對照（去掉 TCN encoder）

## 子封包

| 套件 | 主題 |
|---|---|
| v13_moco_fusion_package | MoCo pretrained + GMU/Sum |
| v13a_gradcam_diagnosis | GradCAM 視覺解釋（無 metric）|
| v13b_caxton_l27_image_only_runs | CAXTON L27 + image only |
| v13c_domain_adversarial_package | Domain adversarial training |
| v13d_clean_data_package | ★ 最終乾淨資料 baseline |
| v13e_imgonly_comparison_package | Image-only 對照 |

## 全 run 表格

| package                         | run_id                                        | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:--------------------------------|:----------------------------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v13d_clean_data_package         | v13d_gmu_moco_pretrained_include64train_seed3 | moco_pretrained      | gmu             |                          0.9411 |                                    0.5119 |                                                 nan |                                                nan |
| v13d_clean_data_package         | v13d_gmu_moco_pretrained_include64train_seed2 | moco_pretrained      | gmu             |                          0.9537 |                                    0.5086 |                                                 nan |                                                nan |
| v13d_clean_data_package         | v13d_gmu_moco_pretrained_include64train_seed1 | moco_pretrained      | gmu             |                          0.9346 |                                    0.4554 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_moco_pretrained_include64train_seed3  | moco_pretrained      | gmu             |                          0.9144 |                                    0.4154 |                                                 nan |                                                nan |
| v13c_domain_adversarial_package | v13c_gmu_moco_pretrained_seed3                | moco_pretrained      | gmu             |                          0.9268 |                                    0.4120 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_moco_pretrained_include64train_seed2  | moco_pretrained      | gmu             |                          0.9378 |                                    0.4104 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_moco_pretrained_include64train_seed1  | moco_pretrained      | gmu             |                          0.9195 |                                    0.3932 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_moco_pretrained_include64train_seed5  | moco_pretrained      | gmu             |                          0.9320 |                                    0.3870 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_scratch_include64train_seed3          | scratch              | gmu             |                          0.9393 |                                    0.3783 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_moco_pretrained_include64train_seed4  | moco_pretrained      | gmu             |                          0.9413 |                                    0.3780 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_moco_pretrained_include64train_seed4  | moco_pretrained      | sum             |                          0.9047 |                                    0.3643 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_scratch_include64train_seed2          | scratch              | gmu             |                          0.9436 |                                    0.3609 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_moco_pretrained_include64train_seed2  | moco_pretrained      | sum             |                          0.9303 |                                    0.3602 |                                                 nan |                                                nan |
| v13c_domain_adversarial_package | v13c_gmu_moco_pretrained_seed1                | moco_pretrained      | gmu             |                          0.9436 |                                    0.3563 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_scratch_include64train_seed1          | scratch              | gmu             |                          0.9438 |                                    0.3530 |                                                 nan |                                                nan |
| v13c_domain_adversarial_package | v13c_gmu_moco_pretrained_seed2                | moco_pretrained      | gmu             |                          0.9400 |                                    0.3527 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_moco_pretrained_include64train_seed3  | moco_pretrained      | sum             |                          0.9279 |                                    0.3526 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_moco_pretrained_include64train_seed1  | moco_pretrained      | sum             |                          0.9377 |                                    0.3508 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_moco_pretrained_include64train_seed5  | moco_pretrained      | sum             |                          0.9220 |                                    0.3479 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_scratch_include64train_seed4          | scratch              | gmu             |                          0.9593 |                                    0.3396 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_gmu_scratch_include64train_seed5          | scratch              | gmu             |                          0.9613 |                                    0.3254 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_scratch_include64train_seed1          | scratch              | sum             |                          0.9331 |                                    0.3206 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_scratch_include64train_seed3          | scratch              | sum             |                          0.9350 |                                    0.3187 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_scratch_include64train_seed2          | scratch              | sum             |                          0.9423 |                                    0.3013 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_scratch_include64train_seed4          | scratch              | sum             |                          0.9630 |                                    0.3009 |                                                 nan |                                                nan |
| v13_moco_fusion_package         | v13_sum_scratch_include64train_seed5          | scratch              | sum             |                          0.9630 |                                    0.2949 |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | caxton_imgonly_seed1                          | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | caxton_imgonly_seed2                          | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | caxton_imgonly_seed3                          | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | v13d_imgonly_seed1                            | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | v13d_imgonly_seed2                            | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |
| v13e_imgonly_comparison_package | v13d_imgonly_seed3                            | nan                  | nan             |                        nan      |                                  nan      |                                                 nan |                                                nan |

## v13d 是 MobileNet 時代的 baseline

**MobileNetV3 + MoCo + GMU 的最佳組合**：
- id_val avg4: ~0.93-0.95
- holdout avg4: **~0.51（隨機 seed 之間 0.46-0.51）**
- holdout flow: ~0.01（完全不會泛化）
- holdout tension: ~0.95（MobileNet 反而沒被 capacity-aliased shortcut 害到）

## 主要限制

- **Flow head 在 holdout 完全失效**（balanced acc ≈ 0）
- MobileNet image encoder 無法區分視覺上接近的 flow 90/100/110

## 結論：需要更強的 image encoder

→ v15 切換到 DINOv2 ViT 是直接後果。
