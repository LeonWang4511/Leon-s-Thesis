"""Add Jekyll just-the-docs front matter to every .md file in the repo.

This sets nav_order, parent, has_children correctly for sidebar navigation.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file_path_relative_to_root, title, nav_order, parent, has_children)
PAGES = [
    # Home is index.md (generated separately)
    ("00_INDEX.md",                                "0. 總導覽",            1, None, False),
    ("01_data_design.md",                          "1. 資料設計 L9",       2, None, False),
    ("12_shortcut_learning_diagnosis.md",          "★ Shortcut Learning 診斷",  3, None, False),
    ("15_all_metrics_summary.md",                  "★ 全指標彙整",          4, None, False),
    ("14_onnx_deployment.md",                      "ONNX 部署",            5, None, False),
    ("13_tcn_v1_fault_detector.md",                "TCN_v1 故障偵測",       6, None, False),
    ("16_lessons_learned.md",                      "★ 經驗總結",           7, None, False),
    # Version history parent
    ("02_legacy_v1_to_v10.md",                     "v1-v10 早期",          1, "版本演進 (Version History)", False),
    ("versions/03_v11_mobilenet_series.md",        "v11 MobileNet 系列",   2, "版本演進 (Version History)", False),
    ("versions/04_v12_fusion_comparison.md",       "v12 Fusion 比較",      3, "版本演進 (Version History)", False),
    ("versions/05_v13_moco_clean_data.md",         "v13 MoCo + Clean",     4, "版本演進 (Version History)", False),
    ("versions/06_v14_seqnorm_flow.md",            "v14 SeqNorm",          5, "版本演進 (Version History)", False),
    ("versions/07_v15_dinov2_introduction.md",     "v15 DINOv2 引入",      6, "版本演進 (Version History)", False),
    ("versions/08_v16_dinov3.md",                  "v16 DINOv3",           7, "版本演進 (Version History)", False),
    ("versions/09_v17_canonical_5blk.md",          "★ v17 Canonical 5blk", 8, "版本演進 (Version History)", False),
    ("versions/10_v18_to_v23_extensions.md",       "v18-v23 擴展",         9, "版本演進 (Version History)", False),
    ("versions/11_v24_shallow_wide.md",            "★ v24 部署優化",       10, "版本演進 (Version History)", False),
    ("versions/legacy_v1_to_v6_summary_zh.md",     "v1-v6 中文摘要",       11, "版本演進 (Version History)", False),
]


def write_with_bom(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8-sig")


def add_front_matter(path: Path, fm: str) -> None:
    raw_bytes = path.read_bytes()
    # Strip BOM if present so we can prepend front matter cleanly
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        text = raw_bytes[3:].decode("utf-8")
    else:
        text = raw_bytes.decode("utf-8")
    # Remove existing front matter if any
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            text = text[end + 5:]
    full = fm + "\n" + text
    write_with_bom(path, full)


def main():
    # Write parent stub for "版本演進"
    parent_md = """---
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
"""
    write_with_bom(ROOT / "versions_index.md", parent_md)

    # Apply front matter to all listed pages
    for rel, title, order, parent, has_children in PAGES:
        path = ROOT / rel
        if not path.exists():
            print(f"  SKIP missing: {rel}")
            continue
        fm_lines = ["---", f"title: {title}", f"nav_order: {order}"]
        if parent:
            fm_lines.append(f"parent: {parent}")
        if has_children:
            fm_lines.append("has_children: true")
        fm_lines.append("---")
        fm = "\n".join(fm_lines)
        add_front_matter(path, fm)
        print(f"  patched: {rel}")

    print("[front-matter] done")


if __name__ == "__main__":
    main()
