# 07 — v15 DINOv2 ViT 切換

## 動機

MobileNet 卡住。改用 self-supervised pretrained ViT（DINOv2 ViT-S/14）試圖解決 flow head。

## 子封包

| 套件 | 主題 |
|---|---|
| v15_dinov2_vit_package | DINOv2 ViT-S/14 baseline + mixup |
| v15a_unfreeze_domadv_package | Unfreeze + domain adversarial |
| v15b_ablation_package | Frozen / partial CAXTON adaptation |
| v15c_dualenc_package | ★ Dual encoder branch A/B（後續 v17 採用此架構）|

## 全 run 表格

| package                      | run_id                        | image_encoder_init   | fusion_method   |   id_val_avg4_balanced_accuracy |   internal_holdout_avg4_balanced_accuracy |   internal_holdout_param_ood_avg4_balanced_accuracy |   internal_holdout_geom_ood_avg4_balanced_accuracy |
|:-----------------------------|:------------------------------|:---------------------|:----------------|--------------------------------:|------------------------------------------:|----------------------------------------------------:|---------------------------------------------------:|
| v15c_dualenc_package         | v15c_dualenc_seed1            | dinov2_dual          | vit_dual        |                          0.7305 |                                    0.7863 |                                              0.7677 |                                             0.8083 |
| v15c_dualenc_package         | v15c_dualenc_temporal_seed1   | dinov2_dual          | vit_dual        |                          0.9133 |                                    0.6973 |                                              0.6802 |                                             0.7175 |
| v15_dinov2_vit_package       | v15_dinov2_vit_seed1          | dinov2_pretrained    | vit             |                          0.8528 |                                    0.5126 |                                            nan      |                                           nan      |
| v15b_ablation_package        | v15b_normonly_caxton_seed1    | dinov2_norm_only     | vit             |                          0.8517 |                                    0.5020 |                                            nan      |                                           nan      |
| v15_dinov2_vit_package       | v15_dinov2_vit_mixup_seed1    | dinov2_pretrained    | vit_mixup       |                          0.7906 |                                    0.5017 |                                            nan      |                                           nan      |
| v15b_ablation_package        | v15b_frozen_caxton_seed1      | dinov2_frozen        | vit             |                          0.8408 |                                    0.4899 |                                            nan      |                                           nan      |
| v15a_unfreeze_domadv_package | v15a_unfreeze_caxton_seed1    | dinov2_partial       | vit             |                          0.9872 |                                    0.4303 |                                            nan      |                                           nan      |
| v15b_ablation_package        | v15b_partial_caxton_w05_seed1 | dinov2_partial       | vit             |                          0.9903 |                                    0.4132 |                                            nan      |                                           nan      |

## 重大突破：v15c dual-encoder

**v15c_dualenc** 把 ViT 分成 branch A (frozen, 給 speed/flow/temp) 和 branch B (trainable, 給 tension)：
- 內部 holdout avg4: **0.786**（v15 系列最高，也是當時 SOTA）
- 比 MobileNet 時代提升 **+0.27 avg4**
- 證明 ViT backbone 是正確方向

## 影響

v17 直接繼承 v15c 的 dual-encoder 設計，加上 truncation 進一步優化。
