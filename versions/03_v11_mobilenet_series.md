# 03 — v11 系列：MobileNetV3 多頭協議

## 動機

v10 之後將協議統一到 4 個 head（speed/flow/temp/tension）。v11 系列做了：
- L27 / L9 protocol 比較
- Per-head 分析
- Sampling 比例調整 (0.4 sampling)
- Two-contrast label audit
- ImageNet vs MoCo source backbone 對比
- Teacher distillation
- Loss followup（class3 margin, print-balanced CE 等）

## 核心子封包

| 套件 | 主題 |
|---|---|
| v11_tension_protocol_package | Tension 協議建立 |
| v11a_expanded_nature_codex_package | Nature paper baseline 重現擴展 |
| v11b_complete_l27_codex_package_v2 | 完整 L27 protocol |
| v11c_v5_build | per-head 分析 |
| v11d_0p4_scratch_four_head_build | 0.4 sampling 抽樣 |
| v11d_sampling_0p4_build | 同上 |
| v11e_two_contrast_label_audit_package | 標籤對照修正 |
| v11f_transfer_64audit_package | ImageNet/Scratch transfer 對比 |
| v11f_mobilenet_nature_transfer_64audit_package | nature backbone transfer |
| v11f_mobilenet_teacher_distill_64audit_package | Teacher distillation |
| v11g_loss_followup_package | Loss 跟進實驗 |

## 全 run 表格

| package                                        | run_id                                                        |   image_encoder_init |   fusion_method |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-----------------------------------------------|:--------------------------------------------------------------|---------------------:|----------------:|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v11c_v5_build                                  | nature_finetune_tension_only_seed1                            |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_finetune_tension_only_seed2                            |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_finetune_tension_only_seed3                            |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_linear_seed1                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_linear_seed2                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_linear_seed3                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_mlp_seed1                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_mlp_seed2                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | nature_frozen_mlp_seed3                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_linear_seed1                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_linear_seed2                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_linear_seed3                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_mlp_seed1                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_mlp_seed2                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | random_frozen_mlp_seed3                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_four_head_seed1                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_four_head_seed2                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_four_head_seed3                                       |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_tension_only_seed1                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_tension_only_seed2                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11c_v5_build                                  | scratch_tension_only_seed3                                    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11d_0p4_scratch_four_head_build               | scratch_four_head_0p4_seed1                                   |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11d_0p4_scratch_four_head_build               | scratch_four_head_0p4_seed2                                   |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11d_0p4_scratch_four_head_build               | scratch_four_head_0p4_seed3                                   |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed1                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed2                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed3                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed1                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed2                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed3                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed1                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed2                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_include64train_seed3                        |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed1                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed2                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11e_two_contrast_label_audit_package          | scratch_four_head_quarantine64_seed3                          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_mobilenet_teacher_distill_64audit_package | mobilenetv3small_scratch_include64train_seed1                 |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_mobilenet_teacher_distill_64audit_package | mobilenetv3small_scratch_quarantine64_seed1                   |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_mobilenet_teacher_distill_64audit_package | mobilenetv3small_teacherdistill_include64train_seed1          |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_mobilenet_teacher_distill_64audit_package | mobilenetv3small_teacherdistill_quarantine64_seed1            |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_transfer_64audit_package                  | mobilenetv3small_imagenet_include64train_seed1                |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_transfer_64audit_package                  | mobilenetv3small_imagenet_quarantine64_seed1                  |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_transfer_64audit_package                  | mobilenetv3small_scratch_include64train_seed1                 |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11f_transfer_64audit_package                  | mobilenetv3small_scratch_quarantine64_seed1                   |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11g_loss_followup_package                     | v11g_mobilenetv3small_printbalancedce_include64train_seed1    |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |
| v11g_loss_followup_package                     | v11g_mobilenetv3small_tensiononlydistill_include64train_seed1 |                  nan |             nan |                             nan |                                       nan |                                                 nan |                                                nan |

## 主要發現

1. **MobileNetV3 + Image-only 在 tension 上接近完美，但 flow / temp 在 holdout 崩**
2. **Teacher distillation 微幅幫助 tension，對其他頭幫助有限**
3. **Print-balanced CE / class3 margin 修正 class imbalance** — 對 holdout 有限改善
4. **這時期建立了 train/val/test/holdout 切法的最終版**（random_session_split seed=12345）

## 關鍵結論

MobileNet capacity 不足以區分 flow 90/100/110 的視覺差異 → 後續需要更強的 image encoder（v15+ ViT）。
