---
title: v14 SeqNorm
nav_order: 5
parent: 版本演進 (Version History)
---

# v14 — Sequence Normalization + Flow Image 嘗試

## 動機

- **v14**: sequence-level instance normalization
- **v14a**: CAXTON-style augmentation
- **v14b**: Seq aug + full instance norm
- **v14c**: Seq aug + image aug 組合

## v14 系列最佳 5 runs

| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |
|---|---|---|---:|---:|---:|---:|
| `v14_tcnonly_instanorm_seed1` | scratch | tcnonly | 0.6844 | **0.5222** | — | — |
| `v14_aonly_moco_pretrained_seed` | moco_pretrained | aonly | 0.9529 | **0.5185** | — | — |
| `v14_tcnonly_instanorm_seed3` | scratch | tcnonly | 0.7207 | **0.5154** | — | — |
| `v14_tcnonly_instanorm_seed2` | scratch | tcnonly | 0.6752 | **0.5118** | — | — |
| `v14_perheadgmu_moco_pretrained` | moco_pretrained | perheadgmu | 0.9494 | **0.5050** | — | — |


## 主要發現

- Sequence instance norm 對 **encoder-only** 有幫助（v14_tcnonly_instanorm 在 flow 反而比 MobileNet+TCN 好）
- **Augmentation 提升有限**，無法解決 image encoder 對 flow 的根本不足
- v14 確認問題在 image encoder（不是 fusion 或 normalization）

## 為什麼這時期 plateau

整個 v11-v14 都用 **MobileNetV3-Small backbone**（為了部署考量）。
flow head 的視覺信號需要更強的 backbone 才能學起來。
