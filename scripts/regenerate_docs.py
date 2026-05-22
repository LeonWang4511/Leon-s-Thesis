"""Regenerate docs with clean, narrative-driven content.

Replaces the previous CSV-dump style with hand-curated tables that render
cleanly in just-the-docs sidebar layout. No wide CSV → markdown blowups.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TBL = ROOT / "tables"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig")
    print(f"  wrote {path.relative_to(ROOT)}")


df_idx = pd.read_csv(TBL / "all_runs_index.csv")


def best_n_for_pkg_prefix(pkg_prefix: str, n: int = 5, sort_by: str = "internal_holdout_avg4_balanced_accuracy") -> list[dict]:
    sub = df_idx[df_idx["package"].str.startswith(pkg_prefix)].dropna(subset=[sort_by]).copy()
    sub = sub.sort_values(sort_by, ascending=False).head(n)
    return sub.to_dict(orient="records")


def fmt(v, prec: int = 4) -> str:
    if v is None or pd.isna(v):
        return "—"
    return f"{v:.{prec}f}"


def best_table_md(pkg_prefix: str, n: int = 5) -> str:
    rows = best_n_for_pkg_prefix(pkg_prefix, n)
    if not rows:
        return "_(無資料)_\n"
    out = "| Run | Encoder | Fusion | id_val | holdout | param_ood | geom_ood |\n"
    out += "|---|---|---|---:|---:|---:|---:|\n"
    for r in rows:
        rid = r["run_id"][:30]
        enc = str(r.get("image_encoder_init", ""))[:20]
        fus = str(r.get("fusion_method", ""))[:10]
        idv = fmt(r.get("id_val_avg4_balanced_accuracy"))
        ih = fmt(r.get("internal_holdout_avg4_balanced_accuracy"))
        po = fmt(r.get("internal_holdout_param_ood_avg4_balanced_accuracy"))
        go = fmt(r.get("internal_holdout_geom_ood_avg4_balanced_accuracy"))
        out += f"| `{rid}` | {enc} | {fus} | {idv} | **{ih}** | {po} | {go} |\n"
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Per-version content (hand-curated narrative + small tables)
# ─────────────────────────────────────────────────────────────────────────────

DOCS = {}

DOCS["versions/03_v11_mobilenet_series.md"] = """---
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

""" + best_table_md("v11", 5) + """

## 主要發現

1. **MobileNetV3 + image-only 在 tension 上接近完美**，但 flow / temp 在 holdout 崩
2. **Teacher distillation** 對 tension 微幫助
3. **Print-balanced CE / class3 margin** 修正 class imbalance — 對 holdout 改善有限
4. 這時期建立了 train/val/test/holdout 切法的最終版（`random_session_split` seed=12345）

## 關鍵結論

MobileNet capacity 不足以區分 flow 90/100/110 的視覺差異 → 後續需要更強的 image encoder。**直接導向 v15 切換到 DINOv2 ViT**。
"""


DOCS["versions/04_v12_fusion_comparison.md"] = """---
title: v12 Fusion 比較
nav_order: 3
parent: 版本演進 (Version History)
---

# v12 — Fusion Mechanism 大比較

## 動機

確定 image + encoder 雙模態必要後，對比不同 fusion 機制：

- **GMU** (Gated Multimodal Unit)
- **FiLM** (Feature-wise Linear Modulation)
- **Sum** (element-wise)
- **Concat** (128 / 256 變體)
- **Hadamard** (element-wise product)
- 加 CAXTON DKD warmup 變體

每個 fusion × scratch / CAXTON pretrained × 3 seeds ≈ 30 runs。

## 架構

- Image encoder: MobileNetV3-Small（frozen 或 CAXTON-adapted）
- TCN: 短 3-layer Conv1d
- Fusion: 變體
- 4 個 Linear heads（speed/flow/temp/tension）

## v12 系列最佳 5 runs

""" + best_table_md("v12", 5) + """

## 主要發現

- **GMU 整體略勝**（id_val 略高，holdout 差距小）
- **FiLM 對某些頭較強**（v17 fusion swap 進一步驗證 FiLM 在 speed/flow 強）
- **CAXTON DKD warmup** 提升有限，但能避免訓練不穩
- **Fusion 選擇影響在 holdout 上小**（差距 < 0.05），瓶頸在 image encoder

## 衍生影響

v17 重做 fusion swap 進一步證實 ── 不同 fusion 在不同 head 強：

| Head | 最強 fusion |
|---|---|
| speed | FiLM |
| flow | FiLM |
| temp | Sum |
| tension | GMU（v17_orig）|

→ v24 採取 **per-head best fusion** 部署策略。
"""


DOCS["versions/05_v13_moco_clean_data.md"] = """---
title: v13 MoCo + Clean Data
nav_order: 4
parent: 版本演進 (Version History)
---

# v13 — MoCo Pretraining + Clean Data 系列

## 動機

- v13: 加入 MoCo self-supervised pretraining
- v13c: 加 domain adversarial
- **v13d: 清洗訓練資料、修正錯誤標籤、最終 MobileNet baseline**
- v13e: 純 image-only 對照

## 子封包

| 套件 | 主題 |
|---|---|
| `v13_moco_fusion_package` | MoCo pretrained + GMU/Sum |
| `v13a_gradcam_diagnosis` | GradCAM 視覺解釋 |
| `v13b_caxton_l27_image_only_runs` | CAXTON L27 + image only |
| `v13c_domain_adversarial_package` | Domain adversarial training |
| `v13d_clean_data_package` | ★ 最終乾淨資料 baseline |
| `v13e_imgonly_comparison_package` | Image-only 對照 |

## v13 系列最佳 5 runs

""" + best_table_md("v13", 5) + """

## v13d — MobileNet 時代最佳 baseline

**MobileNetV3 + MoCo + GMU**:

| 指標 | 數值 |
|---|---:|
| id_val avg4 | 0.93 ~ 0.95 |
| holdout avg4 (best seed) | **0.51** |
| holdout flow | **≈ 0.01** ← 完全不會泛化 |
| holdout tension | ≈ 0.95 |

## 主要限制

- **Flow head 在 holdout 完全失效** (balanced acc ≈ 0)
- MobileNet image encoder 無法區分視覺接近的 flow 90 / 100 / 110

## 結論

需要更強的 image encoder → **v15 切換到 DINOv2 ViT 是直接後果**。
"""


DOCS["versions/06_v14_seqnorm_flow.md"] = """---
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

""" + best_table_md("v14", 5) + """

## 主要發現

- Sequence instance norm 對 **encoder-only** 有幫助（v14_tcnonly_instanorm 在 flow 反而比 MobileNet+TCN 好）
- **Augmentation 提升有限**，無法解決 image encoder 對 flow 的根本不足
- v14 確認問題在 image encoder（不是 fusion 或 normalization）

## 為什麼這時期 plateau

整個 v11-v14 都用 **MobileNetV3-Small backbone**（為了部署考量）。
flow head 的視覺信號需要更強的 backbone 才能學起來。
"""


DOCS["versions/07_v15_dinov2_introduction.md"] = """---
title: v15 DINOv2 ViT 引入
nav_order: 6
parent: 版本演進 (Version History)
---

# v15 — DINOv2 ViT 切換 ⚡

## 動機

MobileNet 卡住。改用 self-supervised pretrained ViT (**DINOv2 ViT-S/14**) 試圖解決 flow head。

## 子封包

| 套件 | 主題 |
|---|---|
| `v15_dinov2_vit_package` | DINOv2 ViT-S baseline + mixup |
| `v15a_unfreeze_domadv_package` | Unfreeze + domain adversarial |
| `v15b_ablation_package` | Frozen / partial CAXTON adaptation |
| `v15c_dualenc_package` | ★ Dual encoder branch A/B |

## v15 系列最佳 5 runs

""" + best_table_md("v15", 5) + """

## 重大突破：v15c dual-encoder

**v15c_dualenc** 把 ViT 分成兩個 branch：
- **Branch A** (frozen) → 給 speed/flow/temp
- **Branch B** (trainable) → 給 tension

| 指標 | 數值 |
|---|---:|
| holdout avg4 | **0.786** |
| 跟 MobileNet 時代差距 | **+0.27** |

證明 ViT backbone 是正確方向。

## 影響

**v17 直接繼承 v15c 的 dual-encoder 設計**，加上 truncation 進一步優化。
"""


DOCS["versions/08_v16_dinov3.md"] = """---
title: v16 DINOv3
nav_order: 7
parent: 版本演進 (Version History)
---

# v16 — DINOv3 ViT 切換

## 動機

DINOv2 → **DINOv3**（Meta 2024 新版）。對 OOD 圖像表現更穩定。

## 子封包

| 套件 | 主題 |
|---|---|
| `v16_dinov3_package` | DINOv3 ViT-S/16 完整版 + truncated 6blk |

## v16 系列最佳 5 runs

""" + best_table_md("v16", 5) + """

## 主要發現

- DINOv3 truncated 6blk ≈ DINOv2 full ViT-S
- **Truncation 大幅減少參數**但保留泛化能力
- v17 進一步推到 5blk

## 為什麼 truncate 有效

DINOv3 ViT-S/16 共 **12 blocks**，但對小資料 fine-tuning 而言深層 blocks 反而 overfit。Truncate 到 5-6 個 block 取最佳 trade-off。
"""


DOCS["versions/09_v17_canonical_5blk.md"] = """---
title: v17 Canonical 5blk ★
nav_order: 8
parent: 版本演進 (Version History)
---

# v17 — Canonical Model: DINOv3 5blk Truncated ★

> **本版本為 thesis canonical model**。所有 v18+ 與 v24 都以此為起點。

## 架構

```
Input image (3, 224, 224)
    ↓
DINOv3 ViT-S/16 patch embed
    ↓
Block 0, 1  (shared, frozen)
    ↓
    ├── Branch A: Block 2/3/4 (frozen)    → norm → CLS_a
    └── Branch B: Block 2/3/4 (trainable) → norm → CLS_b

Encoder seq (4 ch, 100 samples = 2s)
    ↓
TCN (3 conv layers)  → seq_vec (96-d)
    ↓
fusion_a = GMU(CLS_a, seq_vec)  → speed / flow / temp heads
fusion_b = GMU(CLS_b, seq_vec)  → tension head
    ↓
4 × Linear(128, 3): speed / flow / temp / tension
```

## 參數量

| 元件 | params | 是否凍結 |
|---|---:|:---:|
| image_encoder (DINOv3 ViT-S/16) | 9,174,528 | ✓ 凍結 |
| blocks_frozen (2 blocks) | 5,325,696 | ✓ 凍結 |
| blocks_trainable (3 blocks) | 5,325,696 | ✗ |
| seq_conv (TCN) | 60,416 | ✗ |
| fusion_a + fusion_b (GMU × 2) | 246,528 | ✗ |
| 4 heads + aux heads | 3,858 | ✗ |
| **Total** | **20,138,258** | (5.64M trainable) |

## 訓練設定

| 項目 | 值 |
|---|---|
| Optimizer | AdamW |
| LR | head=5e-2, feature=5e-3 |
| Weight decay | 1e-4 |
| Schedule | warmup 5 epoch → cosine to 200 |
| Patience | 30 (early stop) |
| Batch | 256 |
| AMP | fp16 enabled |
| Selection | id_val tension balanced accuracy |

## v17 系列最佳 5 runs

""" + best_table_md("v17", 5) + """

## v17_5blk_seed1 全指標（per-frame raw）

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.690 | 0.530 | 0.559 | 0.973 | 0.688 |
| id_test | 0.751 | 0.559 | 0.561 | 0.902 | 0.693 |
| internal_holdout | 0.684 | 0.495 | 0.444 | 0.582 | 0.551 |
| param_ood | 0.685 | 0.490 | 0.352 | 0.672 | 0.550 |
| geom_ood | 0.683 | 0.497 | 0.543 | 0.484 | 0.552 |

## v17_5blk_seed1 全指標（rolling20 + per-head bias）

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.808 | 0.643 | 0.748 | 0.998 | 0.799 |
| id_test | 0.910 | 0.631 | 0.725 | 0.876 | 0.785 |
| internal_holdout | 0.747 | 0.642 | 0.431 | 0.789 | 0.652 |
| param_ood | 0.757 | 0.650 | 0.295 | 0.868 | 0.643 |
| geom_ood | 0.742 | 0.630 | 0.580 | 0.703 | 0.663 |

## 為什麼這版是 canonical

1. **Tension head 在 holdout 0.79 → 全 v17 系列最強**（capacity 剛好，沒被 print-id 過度記憶）
2. **DINOv3 ViT-S vs ViT-B**：ViT-B 更大但 holdout 反而崩
3. **Truncation 5blk** 比 6blk / full 都更好（更輕量也更不易 overfit）
"""


DOCS["versions/10_v18_to_v23_extensions.md"] = """---
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

""" + best_table_md("v18", 3) + """

### v19

""" + best_table_md("v19", 3) + """

### v20

""" + best_table_md("v20", 3) + """

### v22

""" + best_table_md("v22", 3) + """

### v23

""" + best_table_md("v23", 3) + """

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
"""


DOCS["versions/11_v24_shallow_wide.md"] = """---
title: v24 部署優化 ★
nav_order: 10
parent: 版本演進 (Version History)
---

# v24 — Shallow Wide Package: 部署優化 + 多重 Rescue ★

> 本章節是 thesis 的**集大成工程章節**。v17 之後的所有工作都在這個 package。

## v24 系列最佳 5 runs

""" + best_table_md("v24", 5) + """

## 主要工作分類

### A. ViT-B 容量探索（capacity scaling 證據）

| Run | Encoder | Holdout avg4 |
|---|---|---:|
| `v24_dinov2_vitb_5blk` | DINOv2 ViT-B/14 5blk | 0.524 |
| `v24_dinov2_vitb_5blk_warmup15` | + warmup15 | 0.473 |
| `v24_dinov2_vitb_5blk_phase2` | Phase 2 | 0.487 |
| `v24_dinov3_vitb_5blk` | DINOv3 ViT-B/16 5blk | 0.504 |

**結論**：ViT-B 比 ViT-S 差 0.05-0.15。Tension 從 0.58 (ViT-S) 崩到 **0.33** (ViT-B 全部變體)。
→ Shortcut learning 證據（詳見 [Shortcut Learning 診斷](../12_shortcut_learning_diagnosis)）。

### B. Fusion Swap（換 fusion）

| Fusion | Holdout avg4 | tension | flow |
|---|---:|---:|---:|
| GMU (baseline) | 0.580 | 0.525 | 0.601 |
| **FiLM** | 0.560 | 0.398 | **0.643** ← flow 強 |
| **Sum** | 0.567 | 0.434 | 0.629 |
| **Concat_256** | 0.561 | 0.434 | 0.612 |

GMU 整體最強，但 FiLM 在 flow / temp geom_ood 上強。

### C. SGD vs AdamW

| Run | Holdout avg4 |
|---|---:|
| `v17_5blk_sgd_pure_seed1` | 0.580 |
| `v17_5blk_seed1` (AdamW) | 0.551 |

SGD pure 略勝 AdamW。

### D. Rescue 嘗試（全失敗，**temp param_ood 解不開**）

| 嘗試 | 結果 |
|---|---|
| Class bias calibration | helpful，tension 0.58 → 0.79 |
| Per-head best model 選最佳 | helpful，speed/flow 0.69 → 0.85 |
| Center crop TTA | ❌ |
| Geo augmentation 重訓 | ❌ 反而傷 |
| Stacking with InceptionTime/MultiRocket | ❌ |
| Adversarial 拔 speed/flow info | ❌ 全頭崩 |
| Temp head retrain (heavy color jitter) | ❌ 更差 |

### E. Causal Smoothing

| Rolling Window | holdout tension | param_ood | geom_ood |
|---|---:|---:|---:|
| 5s | 0.733 | 0.807 | 0.652 |
| **20s** | **0.788** | **0.868** | **0.702** |
| 50s | 0.822 | 0.894 | 0.745 |
| cumulative | 0.856 | 0.921 | 0.786 |

**rolling20s** 是當前 deployment 配置（trade-off：延遲 vs 準度）。

### F. Per-Head Best Deployment ★

| Head | Model | Bias [0, b1, b2] |
|---|---|---|
| speed | `v17_5blk_film_sgd_seed1` | [0, +0.10, -0.55] |
| flow | `v17_5blk_film_sgd_seed1` | [0, -0.05, -0.15] |
| temp | `v17_5blk_sum_sgd_seed1` | [0, -0.05, -0.20] |
| tension | `v17_5blk_seed1` (v17_orig) | [0, +0.75, +0.65] |

**Per-head best 全指標（rolling20 deployment）**：

| Subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.896 | 0.841 | 0.849 | 0.998 | 0.896 |
| id_test | 0.938 | 0.810 | 0.833 | 0.876 | 0.864 |
| **internal_holdout** | **0.905** | **0.851** | 0.540 | **0.789** | **0.771** |
| **param_ood** | **0.873** | **0.851** | 0.389 | **0.868** | 0.745 |
| **geom_ood** | **0.939** | **0.849** | 0.701 | **0.703** | **0.798** |

✓ **11 / 12 head × subset cells ≥ 70%**

✗ Temp holdout (0.540) 與 temp param_ood (0.389) 是結構性 aliasing 問題
   （詳見 [Shortcut Learning 診斷](../12_shortcut_learning_diagnosis)）

### G. 嚴格 id_val-only 對比（無 holdout leak）

| Subset | avg4 |
|---|---:|
| internal_holdout | 0.644 |
| param_ood | 0.586 |
| geom_ood | 0.706 |

差距：嚴格 id_val 比 holdout-informed 低 ~0.13。Thesis 要老實標註。

### H. ONNX 化（見 [ONNX 部署](../14_onnx_deployment)）

PyTorch fp32 → ONNX fp16：accuracy 差 < 0.001，檔案省 62%。

## 對 thesis 的價值

- 完整 **failure mode 證據**（為什麼 temp param_ood 解不了）
- 完整 **shortcut learning** 量化證據（capacity scaling）
- **per-head best + bias + smoothing** 部署方法論
- **ONNX 化路徑**驗證（部署可行）
"""


DOCS["02_legacy_v1_to_v10.md"] = """---
title: v1-v10 早期
nav_order: 1
parent: 版本演進 (Version History)
---

# v1 - v10 — 早期 MobileNet 嘗試

## 資料來源

`experiment_metrics_audit/` 整理了 v1-v6 共 358 筆實驗 metric。
原始 CSV 已複製到 [`tables/legacy_*.csv`](../tables/).

## 主要技術演進

| 版本 | 主要嘗試 | 結論 |
|---|---|---|
| v1 | MobileNetV3-Small + TCN 多模態 baseline | 確立 image + encoder 雙模態必要性 |
| v2 | 改 preprocessing | 微幅提升 |
| v3-v4 | Source pretraining (Lite CAXTON backbone) | val 上升但 test 提升有限 |
| v5 | 4-head CAXTON source-adapted backbone | 取代 3-head source |
| v5.1-v5.3 | Fusion ablation (M0-M5: image-only, concat, FiLM, cross-attn) | M2 FiLM 略勝 |
| v6 | Tension label 修正（從常數 1 → 真實 2/3/4）+ 全頭訓練 | 重新校準所有比較 |
| v10 | 過渡期，協議統一化 | 為 v11 鋪路 |

## 數據

詳細 358 runs 數據在 [`tables/legacy_all_experiment_metrics.csv`](../tables/legacy_all_experiment_metrics.csv)。

每個 version 最佳 baseline 在 [`tables/legacy_best_by_version.csv`](../tables/legacy_best_by_version.csv)。

## 局限

早期實驗未統一 holdout 切法、tension label 一度有誤、preprocessing 多次變動。
因此 v1-v6 數字**不適合直接跟 v17+ 比較**。

## 引用建議

可在 introduction / related work 提：「我們從 MobileNetV3 + TCN baseline 起步，
經過 v1-v10 的 fusion ablation 與 label 修正，轉向 ViT-based backbone（v15+）」。
"""


# Write all docs
for path_rel, content in DOCS.items():
    write(ROOT / path_rel, content)

print()
print(f"[regenerate] {len(DOCS)} docs regenerated")
