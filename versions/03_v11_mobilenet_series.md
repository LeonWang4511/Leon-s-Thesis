---
title: v11 MobileNet 系列
nav_order: 2
parent: 版本演進 (Version History)
---

# v11 — MobileNetV3 多頭協議建立

## 動機

v10 後協議統一到 4 個 head（speed/flow/temp/tension）。v11 系列各子封包針對：
- L27 / L9 protocol 比較
- Per-head 分析
- Sampling 比例調整 (0.4)
- ImageNet vs MoCo source backbone
- Teacher distillation
- Loss followup（class3 margin, print-balanced CE）

## 子封包

| 套件 | 主題 |
|---|---|
| `v11_tension_protocol_package` | Tension 協議建立 |
| `v11a_expanded_nature_codex_package` | Nature paper baseline 重現 |
| `v11b_complete_l27_codex_package_v2` | 完整 L27 protocol |
| `v11c_v5_build` | per-head 分析 |
| `v11d_*` | 0.4 sampling 抽樣 |
| `v11e_two_contrast_label_audit_package` | 標籤對照修正 |
| `v11f_transfer_64audit_package` | ImageNet/Scratch transfer |
| `v11f_mobilenet_nature_transfer_64audit_package` | nature backbone transfer |
| `v11f_mobilenet_teacher_distill_64audit_package` | Teacher distillation |
| `v11g_loss_followup_package` | Loss 跟進實驗 |

## v11 系列最佳 5 runs

_(無資料)_


## 主要發現

1. **MobileNetV3 + image-only 在 tension 上接近完美**，但 flow / temp 在 holdout 崩
2. **Teacher distillation** 對 tension 微幫助
3. **Print-balanced CE / class3 margin** 修正 class imbalance — 對 holdout 改善有限
4. 這時期建立了 train/val/test/holdout 切法的最終版（`random_session_split` seed=12345）

## 關鍵結論

MobileNet capacity 不足以區分 flow 90/100/110 的視覺差異 → 後續需要更強的 image encoder。**直接導向 v15 切換到 DINOv2 ViT**。
