---
title: 版本演進 (Version History)
nav_order: 8
has_children: true
permalink: /versions/
---

# 版本演進 (Version History)

從 v1 (MobileNetV3 baseline) 到 v24 (DINOv3 ViT-S 5blk + per-head best deployment) 的完整研究路徑。

## 演進總覽

```
v1-v10  ──→  MobileNetV3-Small + TCN，多頭分類概念建立
            │
v11-v14 ──→  Fusion 比較、MoCo、Loss 嘗試（MobileNet 卡 flow head）
            │
v15     ──→  ⚡ DINOv2 ViT-S 切換，dual encoder 設計（avg4 +0.27）
            │
v16     ──→  DINOv3 ViT-S 升級
            │
v17     ──→  ★ Truncate 到 5 blocks (current canonical)
            │
v18-v23 ──→  Augmentation, attention, capacity 上限探索（plateau）
            │
v24     ──→  ★ Per-head best deployment + shortcut learning 診斷 + ONNX 化
```

## 各版本詳細記錄

從左側導覽列點選任一版本，或依時序往下閱讀。

| 版本 | 重點 |
|---|---|
| [v1-v10](02_legacy_v1_to_v10) | 早期 MobileNet 探索 |
| [v11 MobileNet 系列](versions/03_v11_mobilenet_series) | Per-head 協議、Transfer 嘗試 |
| [v12 Fusion 比較](versions/04_v12_fusion_comparison) | GMU / FiLM / Sum / Concat |
| [v13 MoCo + Clean](versions/05_v13_moco_clean_data) | MoCo pretrain，最終 MobileNet baseline |
| [v14 SeqNorm](versions/06_v14_seqnorm_flow) | Sequence normalization |
| [v15 DINOv2](versions/07_v15_dinov2_introduction) | ⚡ ViT 切換 |
| [v16 DINOv3](versions/08_v16_dinov3) | DINOv3 升級 |
| [**v17 Canonical**](versions/09_v17_canonical_5blk) | ★ 5blk truncated，current baseline |
| [v18-v23 擴展](versions/10_v18_to_v23_extensions) | Plateau 探索 |
| [**v24 部署優化**](versions/11_v24_shallow_wide) | ★ Per-head best + shortcut diagnosis |
| [v1-v6 中文摘要](versions/legacy_v1_to_v6_summary_zh) | 早期 audit |
