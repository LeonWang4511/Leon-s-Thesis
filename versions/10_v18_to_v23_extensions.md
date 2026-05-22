---
title: v18-v23 擴展
nav_order: 9
parent: 版本演進 (Version History)
---

# v18-v23 — 各種擴展嘗試

## 各擴展套件

| 套件 | 主題 | 結論 |
|---|---|---|
| v18_dinov2_augmentation_package | mixup / cutmix / geometric | mixup holdout 0.719 |
| v19_flow_targeted_aug_package | flow-targeted augmentation | F1 變體 0.670 |
| v20_arch_gradcam_study_package | 架構變體 + GradCAM | 2-branch noseq 0.652 |
| v22_se_attention_package | SE attention | SE_cls 0.755 |
| v23_dinov2_vitl_ceiling_package | ViT-L 上限探索 | 容量過大 overfit |

## v18 - v23 最佳各 3 runs

### v18

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v18_mixup_seed1` | dinov2_dual | vit_dual | 0.6867 | **0.7190** | 0.7194 | 0.7199 |
| `v18_cutmix_seed1` | dinov2_dual | vit_dual | 0.6010 | **0.7054** | 0.6761 | 0.7401 |
| `v18_geometric_seed1` | dinov2_dual | vit_dual | 0.5974 | **0.6914** | 0.6655 | 0.7218 |


### v19

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v19_F1_seed1` | dinov2_dual | vit_dual | 0.5910 | **0.6699** | 0.6549 | 0.6875 |


### v20

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v20_2branch_noseq_seed1` | dinov2_dual | vit_dual | 0.5521 | **0.6518** | 0.6553 | 0.6453 |
| `v20_4branch_seq_seed1` | dinov2_dual | vit_dual | 0.6437 | **0.5855** | 0.5426 | 0.6302 |
| `v20_1branch_seq_seed1` | dinov2_dual | vit_dual | 0.6367 | **0.5483** | 0.5295 | 0.5690 |


### v22

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v22_SE_cls_seed1` | dinov2_dual | vit_dual | 0.6862 | **0.7547** | 0.7250 | 0.7898 |


### v23

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v23_dinov2_vitl_ceiling_seed1` | dinov2_vitl_dual | vit_dual | 0.6244 | **0.5048** | 0.4804 | 0.5301 |


## 主要發現

1. **Augmentation 邊際效應遞減**：mixup ~0.72, geometric ~0.69，沒突破 v15c dualenc 的 0.78
2. **SE attention 略幫助**（v22 0.755）
3. **ViT-L 反而更差** — capacity scaling 揭示 shortcut learning
4. **架構優化邊際**：2-branch / 4-branch 都沒明顯突破

## 影響

v18-v23 的探索讓我們意識到：

- 模型架構在這個資料規模下**已接近天花板**
- 真正瓶頸在資料設計（L9 aliasing）和小樣本
- **→ 轉向 v24 的 deployment 優化 + shortcut learning 診斷**
