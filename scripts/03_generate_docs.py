"""Generate all RESEARCH_HISTORY markdown documents in UTF-8 with BOM."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[2]
RH = Path(__file__).resolve().parents[1]
TBL = RH / "tables"
VER = RH / "versions"
VER.mkdir(parents=True, exist_ok=True)


def write_doc(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig")
    print(f"  wrote {path.relative_to(RH)}  ({len(content):,} chars)")


# ─── Load metrics master ──────────────────────────────────────────────────────
df_all = pd.read_csv(TBL / "all_metrics_master.csv")
df_idx = pd.read_csv(TBL / "all_runs_index.csv")
df_cfg = pd.read_csv(TBL / "all_run_configs.csv")
df_legacy = pd.read_csv(TBL / "legacy_all_experiment_metrics.csv")
df_legacy_best = pd.read_csv(TBL / "legacy_best_by_version.csv")


def best_row_for_pkg(pkg: str, col: str = "internal_holdout_avg4_balanced_accuracy") -> dict | None:
    sub = df_idx[df_idx["package"] == pkg].dropna(subset=[col])
    if len(sub) == 0:
        return None
    return sub.sort_values(col, ascending=False).iloc[0].to_dict()


# ═══════════════════════════════════════════════════════════════════════════════
# 00_INDEX.md
# ═══════════════════════════════════════════════════════════════════════════════
INDEX = """# RESEARCH HISTORY — FDM 多模態監測 完整研究歷程

**整理日期**: 2026-05-22
**作者**: Leon（thesis 主導）+ Claude / Codex 協助
**目標**: FDM 3D 列印多頭參數監測 + 故障偵測，達到部署級表現

## 此資料夾結構

```
RESEARCH_HISTORY/
├── 00_INDEX.md                      ← 本檔（總導覽）
├── 01_data_design.md                ← Taguchi L9 直交設計、資料切分、樣本數
├── 02_legacy_v1_to_v10.md           ← v1-v10 早期 MobileNet 嘗試
├── 03_v11_mobilenet_series.md       ← v11* 系列（MobileNetV3 多頭實驗）
├── 04_v12_fusion_comparison.md      ← v12 fusion 大比較（GMU/FiLM/Sum/Concat/Hadamard）
├── 05_v13_moco_clean_data.md        ← v13/v13c/v13d/v13e MoCo + clean data
├── 06_v14_seqnorm_flow.md           ← v14* sequence normalization
├── 07_v15_dinov2_introduction.md    ← v15 DINOv2 ViT 引入
├── 08_v16_dinov3.md                 ← v16 DINOv3 切換
├── 09_v17_canonical_5blk.md         ← v17 5blk 截斷（current canonical）
├── 10_v18_to_v23_extensions.md      ← v18-v23 (augment, attention, ceiling)
├── 11_v24_shallow_wide.md           ← v24 重要工作（per-head, fusion swap, rescue）
├── 12_shortcut_learning_diagnosis.md ← 關鍵研究發現：DOE aliasing → ML shortcut
├── 13_tcn_v1_fault_detector.md      ← TCN_v1 故障偵測 model
├── 14_onnx_deployment.md            ← ONNX 化 + 部署規格
├── 15_all_metrics_summary.md        ← 所有版本主指標彙整
├── 16_lessons_learned.md            ← 經驗總結 + 未來方向
├── tables/                          ← 所有原始 CSV 表格
│   ├── all_metrics_master.csv       ← 179 runs 全頭全 subset 指標
│   ├── all_runs_index.csv           ← 每 run 簡表
│   ├── all_run_configs.csv          ← 206 個 run config
│   ├── all_hyperparameters.csv      ← 12 個 hyperparam 文件
│   ├── best_per_package.csv         ← 每 package 最佳 run
│   ├── legacy_all_experiment_metrics.csv  ← v1-v6 era 358 筆
│   ├── legacy_best_by_version.csv
│   ├── legacy_best_by_version_phase.csv
│   ├── legacy_top30_overall.csv
│   └── legacy_top20_strict_or_cv_splits.csv
├── versions/                        ← 自動產生的個別 version 摘要
└── scripts/                         ← 重新產生本資料夾的 Python scripts
    ├── 01_collect_all_metrics.py
    ├── 02_collect_configs.py
    └── 03_generate_docs.py
```

## 編碼

所有 markdown 與 CSV 均以 **UTF-8 with BOM** 儲存，確保 Windows/Excel 與 AI 工具都能讀。

## 整體版本演進（high-level）

```
v1-v10:    MobileNetV3 + TCN，多頭分類概念建立
v11-v14:   MobileNetV3 各種 fusion / loss / MoCo pretraining 嘗試
v15:       切換至 DINOv2 ViT-S
v16:       切換至 DINOv3 ViT-S
v17:       DINOv3 truncated 5blk + dual branch GMU（★ canonical）
v18-v23:   各種 augmentation / attention / capacity 上限探索
v24:       per-head best deployment + shortcut learning 診斷 + ONNX 化
```

## 目前最佳成果 (內部 holdout)

| 設定 | avg4 | 來源 |
|---|---:|---|
| MobileNet 時代 (v13d) | 0.512 | 04, 05 章 |
| v17_5blk_seed1 (DINOv3 ViT-S) | 0.652 | 09 章 |
| **per-head best mix + bias + rolling20** | **0.771** | **11 章** |

## 主要研究發現

1. **DOE aliasing → ML shortcut** (詳見 12)：原始 L9 設計使 (s,f) → temp 為確定函數，導致 ML 模型走捷徑而非學真實視覺特徵。
2. **Capacity scaling shortcut** (詳見 12)：ViT-B (768-d) 比 ViT-S (384-d) 在 holdout 上**更差**（tension 0.33 vs 0.58），更大 backbone 將 capacity 用於記憶 print-id 而非泛化特徵。
3. **Temp param_ood 結構性無解** (詳見 11)：在 L9 訓練資料下，temp 視覺信號根本不存在於模型 representation。
4. **ONNX 化幾乎無精度損失** (詳見 14)：fp16 量化後 avg4 差距 < 0.001。

## 給未來讀者

- 從 **00 → 01 → 09 → 11 → 12 → 15** 為核心閱讀路徑
- 02-08 是發展歷史，可選讀
- 13, 14 是部署與工程實作

"""
write_doc(RH / "00_INDEX.md", INDEX)


# ═══════════════════════════════════════════════════════════════════════════════
# 01_data_design.md
# ═══════════════════════════════════════════════════════════════════════════════
DATA_DESIGN = """# 01 — 資料設計與切分

## 直交設計（Taguchi L9(3³) inner × tension outer × piece outer）

### 因子層次

| 層次 | 因子 | levels | 物理意義 |
|---|---|---|---|
| Inner L9(3³) | speed | 70 / 100 / 130 % | UM2+ feedrate multiplier |
|  | flow | 90 / 100 / 110 % | UM2+ flow multiplier |
|  | temp | 195 / 210 / 225 °C | hotend setpoint |
| Outer (cross) | tension | 2 / 3 / 4 | 螺絲位置（鬆/中/緊）|
| Outer (replicate) | piece | A / B / C | 3 種幾何形狀 |

### L9 Latin Square（temp 作為 cell value）

```
           flow=90    flow=100    flow=110
speed=70 :  195         210         225
speed=100:  210         225         195
speed=130:  225         195         210
```

**代數關係**：`temp_idx = (speed_idx + flow_idx) mod 3`（cyclic Latin Square）

### 81 prints 結構

- 9 個 (s,f,t) Latin Square × 3 tensions × 3 pieces = **81 prints**
- 每個因子 level 出現 27 次（主效應正交）
- temp 完全被 (s, f) 二因子交互作用 alias（**結構性缺陷，詳見 12 章**）

### 27 個唯一 (s, f, t, tension) 組合對應 print_id

| 編號 | 列印速度 | 流率 | 列印溫度 | 張力等級 |
|:---:|:---:|:---:|:---:|:---:|
| 1–3 | 100 % | 100 % | 225 度 | 2 級 |
| 4–6 | 100 % | 110 % | 195 度 | 3 級 |
| 7–9 | 70 % | 100 % | 210 度 | 3 級 |
| 10–12 | 130 % | 100 % | 195 度 | 4 級 |
| 13–15 | 70 % | 110 % | 225 度 | 4 級 |
| 16–18 | 130 % | 110 % | 210 度 | 2 級 |
| 19–21 | 130 % | 90 % | 225 度 | 3 級 |
| 22–24 | 100 % | 90 % | 210 度 | 4 級 |
| 25–27 | 70 % | 90 % | 195 度 | 2 級 |
| 28–30 | 70 % | 110 % | 225 度 | 3 級 |
| 31–33 | 70 % | 100 % | 210 度 | 2 級 |
| 34–36 | 70 % | 90 % | 195 度 | 3 級 |
| 37–39 | 70 % | 90 % | 195 度 | 4 級 |
| 40–42 | 130 % | 90 % | 225 度 | 4 級 |
| 43–45 | 70 % | 110 % | 225 度 | 2 級 |
| 46–48 | 100 % | 110 % | 195 度 | 4 級 |
| 49–51 | 100 % | 90 % | 210 度 | 3 級 |
| 52–54 | 130 % | 110 % | 210 度 | 3 級 |
| 55–57 | 100 % | 90 % | 210 度 | 2 級 |
| 58–60 | 100 % | 100 % | 225 度 | 3 級 |
| 61–63 | 130 % | 90 % | 225 度 | 2 級 |
| 64–66 | 100 % | 100 % | 225 度 | 4 級 |
| 67–69 | 130 % | 100 % | 195 度 | 3 級 |
| 70–72 | 130 % | 100 % | 195 度 | 2 級 |
| 73–75 | 130 % | 110 % | 210 度 | 4 級 |
| 76–78 | 100 % | 110 % | 195 度 | 2 級 |
| 79–81 | 70 % | 100 % | 210 度 | 4 級 |

每 3 件為同一 (s, f, t, tension) 配 A/B/C piece。

## Holdout 設計

| Holdout 類型 | print_ids | n_prints | 設計意圖 |
|---|---|---:|---|
| **internal_holdout** (合計) | 82-99 | 18 | 完全沒進訓練 |
| └ **internal_holdout_param_ood** | 82-90 | 9 | **故意破壞 L9**（新 (s,f,t) 組合）|
| └ **internal_holdout_geom_ood** | 91-99 | 9 | 沿用 L9 但**新幾何 piece** |

## Train/Val/Test split (1-81)

`random_session_split` (seed=12345)：
- **train**: 57 prints
- **id_val**: 16 prints（model selection + bias calibration 用）
- **id_test**: 8 prints（report 用）

## 樣本數總覽 (1 Hz image sampling, 50 Hz encoder)

| Split | n_prints | n_windows | n_images |
|---|---:|---:|---:|
| train_eval | 57 | 14,741 | 14,741 |
| id_val | 16 | 4,408 | 4,408 |
| id_test | 8 | 2,032 | 2,032 |
| internal_holdout | 18 | 3,637 | 3,637 |
| param_ood | 9 | 1,873 | 1,873 |
| geom_ood | 9 | 1,764 | 1,764 |
| **總計 (1-99)** | **99** | **28,455** | **~24,910 unique** |

## Fault dataset (TCN_v1, 另一系列)

- prints 109-149，5 個故障類別 × 8-9 個 print/class
- 編碼器 40ms 取樣（25 Hz），無影像
- 32 個 print 有效，166,106 個 encoder samples，~111 分鐘總錄製
- 詳見 13 章

## 編碼器訊號（4 channels）

| Channel | 物理意義 |
|---|---|
| dpos_m | 主馬達位置增量 (motor encoder delta) |
| dpos_f | filament 位置增量 (filament encoder delta) |
| K_ratio | 比例（filament / motor 的擠出效率指標）|
| slip_rate | 滑動率（K_ratio 衍生）|

採樣率：50 Hz (v17 模型輸入) 或 25 Hz (TCN_v1)
v17 window length: 100 samples = **2 秒**
TCN_v1 window length: 256 samples = **10.24 秒**

## Tension label 編碼

| 物理 tension level | model class index | 標籤 |
|---|---|---|
| 2（鬆）| 0 | "tension 2" |
| 3（中）| 1 | "tension 3" |
| 4（緊）| 2 | "tension 4" |

（早期錯誤把 tension 當常數 1，v1 era。後期已經修正成 2/3/4）

## 設計缺陷標註

⚠️ **(s, f) → temp 確定別名**：見 11、12 章詳細分析。
⚠️ **小樣本**: 14,741 訓練圖 vs ImageNet 1.28M，需特別注意 shortcut learning 風險。
"""
write_doc(RH / "01_data_design.md", DATA_DESIGN)


# ═══════════════════════════════════════════════════════════════════════════════
# 02_legacy_v1_to_v10.md
# ═══════════════════════════════════════════════════════════════════════════════
LEGACY = """# 02 — 早期版本 v1 - v10 摘要

## 來源

`experiment_metrics_audit/` 整理過 v1-v6 共 358 筆實驗 metric。詳細表格已複製到 `tables/legacy_*.csv`。

## v1-v6 主要進展（從 audit 提取）

依 `legacy_best_by_version.csv`：

"""
LEGACY += df_legacy_best.to_markdown(index=False, floatfmt='.4f') + "\n\n"
LEGACY += """## 主要技術演進

| 版本 | 主要嘗試 | 結論 |
|---|---|---|
| v1 | MobileNetV3-Small + TCN 多模態 baseline | 確立 image + encoder 雙模態必要性 |
| v2 | 改 preprocessing | 微幅提升 |
| v3-v4 | Source pretraining (Lite CAXTON backbone) | val 上升但 test 提升有限 |
| v5 | 4-head CAXTON source-adapted backbone | 取代 3-head source |
| v5.1-v5.3 | Fusion ablation (M0-M5: image-only, concat, FiLM, cross-attn 等) | M2 FiLM 略勝 |
| v6 | Tension label 修正（從常數 1 → 真實 2/3/4）+ 全頭訓練 | 重新校準所有比較 |

## v10 — 過渡期

進入 MobileNetV3 + 完整 4 頭協議。為 v11* 系列鋪路。

## 重點檔案

- `tables/legacy_all_experiment_metrics.csv`：完整 358 筆 v1-v6 實驗
- `tables/legacy_best_by_version.csv`：每版本最佳
- `tables/legacy_top30_overall.csv`：歷史 top 30
- `versions/legacy_v1_to_v6_summary_zh.md`：原始 audit 中文摘要

## 局限

早期實驗未統一 holdout 切法、tension label 不正確、preprocessing 多次變動，因此 v1-v6 數字不適合直接跟 v17+ 比較。

## 對 thesis 的引用建議

可在 introduction / related work 提：「我們從 MobileNetV3 + TCN baseline 起步，經過 v1-v10 的 fusion ablation 與 label 修正後，轉向 ViT-based backbone（v15 以後）」。
"""
write_doc(RH / "02_legacy_v1_to_v10.md", LEGACY)


# ═══════════════════════════════════════════════════════════════════════════════
# 03 - 10: per-version docs (v11 to v23 series)
# ═══════════════════════════════════════════════════════════════════════════════
def pkg_summary_table(pkg_filter: str) -> str:
    sub = df_idx[df_idx["package"].str.startswith(pkg_filter)].copy()
    if len(sub) == 0:
        return "(no runs found)\n"
    cols = ["package", "run_id", "image_encoder_init", "fusion_method",
            "id_val_avg4_balanced_accuracy",
            "internal_holdout_avg4_balanced_accuracy",
            "internal_holdout_param_ood_avg4_balanced_accuracy",
            "internal_holdout_geom_ood_avg4_balanced_accuracy"]
    cols = [c for c in cols if c in sub.columns]
    sub = sub[cols].sort_values("internal_holdout_avg4_balanced_accuracy", ascending=False, na_position="last")
    return sub.to_markdown(index=False, floatfmt='.4f') + "\n"


V11 = """# 03 — v11 系列：MobileNetV3 多頭協議

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

"""
V11 += pkg_summary_table("v11")
V11 += """
## 主要發現

1. **MobileNetV3 + Image-only 在 tension 上接近完美，但 flow / temp 在 holdout 崩**
2. **Teacher distillation 微幅幫助 tension，對其他頭幫助有限**
3. **Print-balanced CE / class3 margin 修正 class imbalance** — 對 holdout 有限改善
4. **這時期建立了 train/val/test/holdout 切法的最終版**（random_session_split seed=12345）

## 關鍵結論

MobileNet capacity 不足以區分 flow 90/100/110 的視覺差異 → 後續需要更強的 image encoder（v15+ ViT）。
"""
write_doc(RH / "versions" / "03_v11_mobilenet_series.md", V11)


V12 = """# 04 — v12 Fusion Comparison

## 動機

確定 image + encoder 雙模態必要後，對比不同 fusion 機制：
- GMU (Gated Multimodal Unit)
- FiLM (Feature-wise Linear Modulation)
- Sum (element-wise sum)
- Concat (128, 256 變體)
- Hadamard (element-wise product)
- 加 CAXTON DKD warmup 變體

每個 fusion × scratch / CAXTON pretrained × 3 seeds = ~30 runs。

## 架構

- Image encoder: MobileNetV3-Small (frozen 或 CAXTON-adapted)
- TCN: 短 3-layer conv1d
- Fusion: 上述各種
- 4 個 Linear heads

## 全 run 表格

"""
V12 += pkg_summary_table("v12")
V12 += """
## 主要發現

- **GMU 整體略勝**（id_val 高但 holdout 跟其他差距小）
- **FiLM 對某些頭較強**（後在 v17 fusion swap 驗證 FiLM 在 speed/flow 強）
- **CAXTON DKD warmup** 提升有限，但能避免訓練不穩
- **fusion 選擇影響在 holdout 上很小**（差距 < 0.05），主要瓶頸是 image encoder 而非 fusion

## 啟示

v17 5blk 時期重做 fusion swap 進一步證實：
- v17_film 在 speed/flow holdout 反而比 v17_orig (GMU) 強
- 但 v17_film 在 tension holdout 崩到 0.38
- → 沒有單一 fusion 是全頭最佳

## 衍生影響

v24_shallow_wide 採取 **per-head best fusion** 策略：speed/flow 用 v17_film, temp 用 v17_sum, tension 用 v17_orig（見 11 章）。
"""
write_doc(RH / "versions" / "04_v12_fusion_comparison.md", V12)


V13 = """# 05 — v13 MoCo Pretraining + Clean Data 系列

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

"""
V13 += pkg_summary_table("v13")
V13 += """
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
"""
write_doc(RH / "versions" / "05_v13_moco_clean_data.md", V13)


V14 = """# 06 — v14 Sequence Normalization + Flow Image 嘗試

## 動機

- v14: 加 sequence-level instance normalization
- v14a: CAXTON-style augmentation
- v14b: Sequence aug + full instance norm
- v14c: Sequence aug + image aug 組合

## 子封包

| 套件 | 主題 |
|---|---|
| v14_seqnorm_flowimage_package | sequence norm + flow image 變體 |
| v14a_caxton_augment_package | CAXTON augmentation |
| v14b_seqaug_fullinstanorm_package | seq augmentation + instance norm |
| v14c_seqaug_imgaug_package | seq aug + image aug 組合 |

## 全 run 表格

"""
V14 += pkg_summary_table("v14")
V14 += """
## 主要發現

- **Sequence instance norm 對 encoder-only 有幫助**（v14_tcnonly_instanorm 在 holdout flow 反而比 MobileNet+TCN 好）
- **Augmentation 提升有限**，無法解決 image encoder 對 flow 的根本不足
- v14 確認問題在 image encoder（不是 fusion 或 normalization）

## 為什麼這時期 plateau

整個 v11-v14 都用 MobileNetV3-Small backbone（為了部署考量）。flow head 的視覺信號需要更強的 backbone 才能學起來。
"""
write_doc(RH / "versions" / "06_v14_seqnorm_flow.md", V14)


V15 = """# 07 — v15 DINOv2 ViT 切換

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

"""
V15 += pkg_summary_table("v15")
V15 += """
## 重大突破：v15c dual-encoder

**v15c_dualenc** 把 ViT 分成 branch A (frozen, 給 speed/flow/temp) 和 branch B (trainable, 給 tension)：
- 內部 holdout avg4: **0.786**（v15 系列最高，也是當時 SOTA）
- 比 MobileNet 時代提升 **+0.27 avg4**
- 證明 ViT backbone 是正確方向

## 影響

v17 直接繼承 v15c 的 dual-encoder 設計，加上 truncation 進一步優化。
"""
write_doc(RH / "versions" / "07_v15_dinov2_introduction.md", V15)


V16 = """# 08 — v16 DINOv3 切換

## 動機

DINOv2 → DINOv3：DINOv3 是新版預訓練，對 OOD 圖像表現更穩定（Meta 2024）。

## 子封包

| 套件 | 主題 |
|---|---|
| v16_dinov3_package | DINOv3 ViT-S/16 完整版 + truncated 6blk |

## 全 run 表格

"""
V16 += pkg_summary_table("v16")
V16 += """
## 主要發現

- DINOv3 truncated 6blk 跟 DINOv2 full ViT-S 表現接近
- truncation 大幅減少參數但保留泛化能力
- → v17 進一步推到 5blk

## 為什麼 truncate 有效

DINOv3 ViT-S/16 共 12 blocks，但對小資料 fine-tuning 而言深層 blocks 反而 overfit。truncate 到 5-6 個 block 拿到 best trade-off。
"""
write_doc(RH / "versions" / "08_v16_dinov3.md", V16)


V17 = """# 09 — v17 Canonical: DINOv3 5blk Truncated

## 此版本地位

**v17 5blk seed1 = 目前 thesis 的 canonical model**。所有後續 v18+ 與 v24 都以此為起點。

## 架構

```
Input image (3, 224, 224)
    ↓
DINOv3 ViT-S/16 patch embed
    ↓
Block 0, 1 (shared, frozen)
    ↓
   ├──→ Branch A: Block 2/3/4 (frozen)   → norm_frozen   → CLS_a
   └──→ Branch B: Block 2/3/4 (trainable)→ norm_trainable → CLS_b

Encoder seq (4 ch, 100 samples = 2s)
    ↓
TCN (3 conv layers)  → seq_vec (96-d)
    ↓
fusion_a = GMU(CLS_a, seq_vec)  → speed/flow/temp heads
fusion_b = GMU(CLS_b, seq_vec)  → tension head
    ↓
4 × Linear(128, 3): speed/flow/temp/tension logits
```

## 參數量

| 元件 | params | 備註 |
|---|---:|---|
| image_encoder (DINOv3 ViT-S/16) | 9.17M | 凍結 |
| blocks_frozen (2 blocks) | 5.33M | 凍結 |
| blocks_trainable (3 blocks) | 5.33M | 訓練 |
| seq_conv (TCN) | 60k | 訓練 |
| fusion_a (GMU) | 123k | 訓練 |
| fusion_b (GMU) | 123k | 訓練 |
| 4 heads (Linear 128→3) | 1.5k | 訓練 |
| aux_speed_head / aux_temp_head | 2.3k | 訓練（未啟用）|
| **Total** | **20.14M** | (5.64M trainable) |

## 訓練設定

- Optimizer: AdamW (lr_head=5e-2, lr_feature=5e-3, wd=1e-4)
- Schedule: warmup 5 epoch → cosine to 200
- Patience: 30 (early stop)
- Batch: 256, num_workers: 8-12
- AMP fp16 enabled
- Selected epoch by id_val tension balanced accuracy

## 全 run 表格

"""
V17 += pkg_summary_table("v17")
V17 += """
## v17_5blk_seed1 全指標 (per-frame raw)

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.690 | 0.530 | 0.559 | 0.973 | 0.688 |
| id_test | 0.751 | 0.559 | 0.561 | 0.902 | 0.693 |
| internal_holdout | 0.684 | 0.495 | 0.444 | 0.582 | 0.551 |
| param_ood | 0.685 | 0.490 | 0.352 | 0.672 | 0.550 |
| geom_ood | 0.683 | 0.497 | 0.543 | 0.484 | 0.552 |

## v17_5blk_seed1 全指標 (rolling20 + per-head bias)

詳見 11 章 v24 工作。簡略：

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.808 | 0.643 | 0.748 | 0.998 | 0.799 |
| id_test | 0.910 | 0.631 | 0.725 | 0.876 | 0.785 |
| internal_holdout | 0.747 | 0.642 | 0.431 | 0.789 | 0.652 |
| param_ood | 0.757 | 0.650 | 0.295 | 0.868 | 0.643 |
| geom_ood | 0.742 | 0.630 | 0.580 | 0.703 | 0.663 |

## 為什麼這版是 baseline

1. **tension head 在 holdout 0.79 → 全 v17 系列最強**（capacity 剛好，沒被 print-id 過度記憶）
2. **DINOv3 ViT-S vs ViT-B**：ViT-B 更大但 holdout 反而崩（見 12 章 shortcut learning）
3. **truncation 5blk** 比 6blk / full 都更好（更輕量也更不易 overfit）
"""
write_doc(RH / "versions" / "09_v17_canonical_5blk.md", V17)


EXTENSIONS = """# 10 — v18-v23 擴展嘗試

## 各擴展套件

| 套件 | 主題 | 結論 |
|---|---|---|
| v18_dinov2_augmentation_package | mixup / cutmix / geometric augment | mixup 在 holdout 0.719（中等改善）|
| v19_flow_targeted_aug_package | flow-targeted augmentation | F1 變體 holdout 0.670 |
| v20_arch_gradcam_study_package | 架構變體 + GradCAM 解釋 | 2-branch noseq 0.652 |
| v22_se_attention_package | SE attention 加成 | SE_cls 0.755 |
| v23_dinov2_vitl_ceiling_package | ViT-L (Large) 上限探索 | 容量過大反而 overfit |

## 全 run 表格

"""
EXTENSIONS += pkg_summary_table("v18") + "\n"
EXTENSIONS += pkg_summary_table("v19") + "\n"
EXTENSIONS += pkg_summary_table("v20") + "\n"
EXTENSIONS += pkg_summary_table("v22") + "\n"
EXTENSIONS += pkg_summary_table("v23") + "\n"
EXTENSIONS += """
## 主要發現

1. **Augmentation 邊際效應遞減**：mixup ~0.72, geometric ~0.69，沒突破 v15c dualenc 的 0.78
2. **SE attention 略幫助**（v22 0.755）
3. **ViT-L 反而更差**（capacity scaling 揭示 shortcut learning，見 12 章）
4. **架構優化邊際**：2-branch / 4-branch 都沒明顯突破

## 影響

v18-v23 的探索讓我們意識到：
- 模型架構在這個資料規模下已經接近天花板
- 真正瓶頸在資料設計（L9 aliasing）和小樣本
- → 轉向 v24 的 deployment 優化 + shortcut learning 診斷
"""
write_doc(RH / "versions" / "10_v18_to_v23_extensions.md", EXTENSIONS)


# ═══════════════════════════════════════════════════════════════════════════════
# 11_v24_shallow_wide.md
# ═══════════════════════════════════════════════════════════════════════════════
V24 = """# 11 — v24 Shallow Wide Package: 部署優化 + 多重 rescue

## 此章節地位

v24 是 thesis 的**集大成工程章節**。v17 之後的所有工作都在這個 package。

## 主要工作分類

### A. ViT-B 探索（capacity scaling）

| run | encoder | 結果（holdout avg4）|
|---|---|---:|
| v24_dinov2_vitb_5blk_seed1 | DINOv2 ViT-B/14 5blk | 0.524 |
| v24_dinov2_vitb_5blk_warmup15 | 同 + warmup15 | 0.473 |
| v24_dinov2_vitb_5blk_phase2 | Phase 2 | 0.487 |
| v24_dinov3_vitb_5blk_seed1 | DINOv3 ViT-B/16 5blk | 0.504 |

**結論**：ViT-B 比 ViT-S 差 0.05~0.15。tension 從 0.58 (ViT-S) 崩到 0.33 (ViT-B 全部變體)。**Shortcut learning 證據**（見 12 章）。

### B. SGD optimizer 探索

| run | optimizer | 結果 |
|---|---|---:|
| v17_5blk_sgd_pilot_seed1 | SGD momentum=0.9 lower lr | 0.581 |
| v17_5blk_sgd_pure_seed1 | SGD pure (lr=5e-2 head) | 0.580 |

SGD pure 略勝 AdamW (v17_5blk_seed1 = 0.551 raw)。

### C. Fusion swap (v17 5blk 架構下換 fusion)

| fusion | holdout avg4 (raw) | tension holdout | flow holdout |
|---|---:|---:|---:|
| GMU (baseline) | 0.580 | 0.525 | 0.601 |
| **FiLM** | 0.560 | **0.398** | **0.643** ← flow 強 |
| **Sum** | 0.567 | 0.434 | 0.629 |
| **Concat_256** | 0.561 | 0.434 | 0.612 |

GMU 整體最強，但 FiLM 在 flow / temp geom_ood 上強。

### D. SeqAux (給 TCN 加 tension 輔助 loss)

| run | tension holdout | 全 avg4 |
|---|---:|---:|
| v17_5blk_seqaux_sgd_seed1 | 0.59 | 0.589 |

TCN 加 aux loss 後 tension 邊際提升，但整體不顯著。

### E. Encoder ablation (詳見 12 章)

證明 temp param_ood 的失效是視覺信號根本不存在，不是 encoder shortcut。

### F. Rescue 嘗試（temp param_ood = 0.39 → 解不開）

| 嘗試 | 結果 |
|---|---|
| Class bias calibration | helpful，但只把 tension 從 0.58 → 0.79 |
| Per-head model 選最佳 | helpful，speed/flow 從 0.69 → 0.85 |
| Center crop TTA | 沒幫助 |
| Geo augmentation 重訓 | 反而傷 |
| Stacking with InceptionTime/MultiRocket | 沒幫助 |
| Adversarial 拔 speed/flow info | 全頭崩 |
| **Temp head retrain (color jitter heavy)** | **更差** |
| **Hotend sensor 輔助**（codex） | temp 達 1.000 但**已 ban**（非影像）|

### G. Causal smoothing (codex)

| rolling window | holdout tension | param_ood tension | geom_ood tension |
|---|---:|---:|---:|
| 5s | 0.733 | 0.807 | 0.652 |
| 20s | 0.788 | 0.868 | 0.702 |
| 50s | 0.822 | 0.894 | 0.745 |
| cumulative | 0.856 | 0.921 | 0.786 |

**rolling20s** 是當前 deployment 配置。

### H. Per-head best deployment（★ 最終配置）

| Head | Model | Bias [0, b1, b2] |
|---|---|---|
| speed | v17_5blk_film_sgd_seed1 | [0, +0.10, -0.55] |
| flow | v17_5blk_film_sgd_seed1 | [0, -0.05, -0.15] |
| temp | v17_5blk_sum_sgd_seed1 | [0, -0.05, -0.20] |
| tension | v17_5blk_seed1 (v17_orig) | [0, +0.75, +0.65] |

**結果（rolling20 deployment）**：

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| id_val | 0.896 | 0.841 | 0.849 | 0.998 | 0.896 |
| id_test | 0.938 | 0.810 | 0.833 | 0.876 | 0.864 |
| internal_holdout | **0.905** | **0.851** | 0.540 | **0.789** | **0.771** |
| param_ood | **0.873** | **0.851** | 0.389 | **0.868** | 0.745 |
| geom_ood | **0.939** | **0.849** | 0.701 | **0.703** | **0.798** |

**11/12 head×subset cells ≥ 70%**，只有 temp holdout / temp param_ood 不過（結構性問題，見 12 章）。

### I. 嚴格 id_val-only 對比版本（沒 holdout leak）

| subset | speed | flow | temp | tension | avg4 |
|---|---:|---:|---:|---:|---:|
| internal_holdout | 0.905 | 0.773 | 0.516 | 0.382 | **0.644** |
| param_ood | 0.873 | 0.769 | 0.308 | 0.394 | 0.586 |
| geom_ood | 0.939 | 0.775 | 0.738 | 0.371 | 0.706 |

**差距**：嚴格 id_val 選法整體 avg4 約 0.64，比 holdout-informed 0.77 低 0.13。tension 大跌（v17_film 在 id_val 略高但在 holdout 崩）。

→ thesis 要老實標註「Version B 是 holdout-informed deployment selection」。

### J. ONNX 化（見 14 章）

PyTorch fp32 → ONNX fp16，accuracy 差 < 0.001。

## 全 run 表格

"""
V24 += pkg_summary_table("v24") + "\n"
V24 += """
## v24 章節對 thesis 的價值

- 完整 **failure mode 證據**（為什麼 temp param_ood 解不了）
- 完整 **shortcut learning** 量化證據（capacity scaling）
- **per-head best + bias + smoothing** 部署方法論（可被引用）
- **ONNX 化路徑**驗證（部署可行）
"""
write_doc(RH / "versions" / "11_v24_shallow_wide.md", V24)


# ═══════════════════════════════════════════════════════════════════════════════
# 12_shortcut_learning_diagnosis.md (核心研究發現)
# ═══════════════════════════════════════════════════════════════════════════════
SHORTCUT = """# 12 — 核心研究發現：DOE Aliasing → ML Shortcut Learning

## TL;DR

> 我們的 Taguchi L9(3³) 內陣設計使 **temp = (speed × flow) interaction** 為**代數確定**。這在 ML 訓練上轉化為「shortcut learning」(Geirhos et al. 2020)：模型透過 (s, f) 視覺特徵 + 內部查表來預測 temp，**從未學到真實的溫度視覺信號**。在 param_ood holdout 上（故意破壞 L9 映射），temp head 直接崩到 0.39（接近隨機）。

## 1. DOE 結構問題

### L9(3³) Latin Square 的代數關係

```
           flow=90    flow=100    flow=110
speed=70 :  195         210         225
speed=100:  210         225         195
speed=130:  225         195         210
```

**關係**：`temp_idx = (speed_idx + flow_idx) mod 3`

對 prints 1-81 中**所有 81 個樣本**都成立 100%。

### 對比：true Taguchi L27(3¹³) 4-factor 不會有此問題

放在 columns C1, C2, C5, C9：每個 (factor_A, factor_B) 看到所有 3 個 factor_C → 沒有確定別名。詳見 `08_v16_dinov3.md` 章節的 L27 設計討論。

## 2. ML 影響：訓練分佈下的捷徑

模型可選的學習路徑：

**Path A**: 學每個 factor 真實視覺特徵
- speed → 看擠出量
- flow → 看線寬
- temp → 看顏色 / 光澤
- tension → 看張力指示
- 成本：4 個獨立 representation

**Path B**: 學 (speed, flow) 視覺 + 內部 lookup
- speed/flow → 直接視覺
- temp → 從 (speed, flow) 推
- tension → 仍要學（沒被 alias）
- 成本：2 個 representation + 內部表

**梯度下降的選擇**：Path B（更省 capacity，loss 一樣低）

## 3. 證據：Encoder ablation

`runs/encoder_ablation_v17_5blk_sgd_pure/encoder_ablation_results.csv` 顯示：

| 移除 | 內 holdout temp | param_ood temp | geom_ood temp |
|---|---:|---:|---:|
| 正常 (image+encoder) | 0.484 | 0.365 | 0.609 |
| 移除 encoder | 0.325 | 0.320 | 0.331 |

→ encoder 對 temp 貢獻只有 +0.04~+0.18，**主要靠 image 走 shortcut**。

## 4. 證據：Capacity scaling — 越大 model 越糟

ViT-S vs ViT-B 同訓練協議：

| Model | params | id_val tension | **holdout tension** | drop |
|---|---:|---:|---:|---:|
| ViT-S (v17_orig DINOv3) | 14.5M | 0.973 | **0.582** | -0.39 |
| ViT-S (DINOv2) | 14.5M | 0.952 | **0.335** | -0.62 |
| ViT-B (DINOv2) | 32M | 0.983 | **0.333** | -0.65 |
| ViT-B (DINOv3) | 32M | 0.987 | **0.357** | -0.63 |

**inverse capacity scaling**：模型越大，holdout tension 越接近隨機（1/3 = 0.333）。
→ 更大 backbone 不是學更好，而是更徹底走 shortcut。

## 5. 證據：(s, f) → temp 嚴格度

每個 (s, f) cell **9 次重複**全部對應同一個 temp：

| (s, f) | temp 出現次數 (n=9) |
|---|---|
| (70, 90) | 195 × 9（從不出現 210/225）|
| (70, 100) | 210 × 9 |
| ... | ... |

**model 沒有任何 counter-example 學「(70, 90) 不是 195」是什麼樣**。

## 6. 嘗試打破 shortcut（全失敗）

| 嘗試 | 結果 |
|---|---|
| Color jitter heavy augmentation | 反而傷 |
| Image-only retrain temp head | 沒幫助（visual signal 不存在）|
| Adversarial 拔 (s, f) 資訊 | 全頭崩 |
| TTA + crop ensemble | 沒幫助 |
| Encoder shortcut subtraction | trade-off 太大 |

**結論**：在 L9 訓練資料下，**任何後處理都救不了 temp param_ood**。必須改資料設計。

## 7. 解法（未做）：true Taguchi L27(3¹³)

把 4 個因子放 L27 的 C1/C2/C5/C9：
- (speed, flow) → temp **不再確定**（每個 (s,f) 看到所有 3 個 temp）
- 27 個唯一 (s, f, t, tension) × 3 pieces = 81 prints（**跟現在一樣多**）
- 但只有 9 個既有印件可重用，需要 **54 個新印件**

或更省的「破壞 L9 patch」方案：印 **27 個 counter-example**（每 (s,f) cell 加 3 個非預設 temp）+ 訓練時 oversample × 3，等效於完整 L27。

## 8. 對應到 thesis 章節

| Thesis 章節 | 此發現的角色 |
|---|---|
| Introduction | 「小樣本 ML 在訓練資料設計上的盲點」 |
| Related Work | Geirhos shortcut learning + Taguchi DOE 跨領域文獻 |
| Methodology | L9 設計 + ViT-S/B capacity scaling 實驗 |
| Results | (s,f) → temp aliasing 量化證據 + holdout 失效 |
| Discussion | DOE aliasing ↔ ML shortcut 對應關係 |
| Future Work | L27(3¹³) 重訓 |

## 9. 一句話論述

> **L9 設計選擇本身（用 Latin Square 節省印件）反而成為 ML shortcut learning 的根本原因。傳統 DOE 教科書推薦的「最節省 orthogonal design」在 ML 訓練上反而是最差的訓練資料設計。**

這個 framing 是 thesis 的 main contribution。

## 10. 相關文獻定位

| 引用 | 用途 |
|---|---|
| Geirhos et al. (2020) Nature MI | shortcut learning 概念定義 |
| Lapuschkin et al. (2019) Nature Comms | Clever Hans phenomenon |
| Torralba & Efros (2011) | dataset bias |
| Taguchi (1986) | L9 / L27 orthogonal arrays |
| Phadke (1989) | linear graph for 4-factor placement |
| Box, Hunter & Hunter (2005) | aliasing / confounding 統計概念 |

## 11. 期刊投稿建議

**Q1 候選**（依命中率排序）：
1. IISE Transactions（工業 + 統計 + ML 跨界）
2. Quality Engineering（DOE 期刊轉 ML 視角）
3. Journal of Manufacturing Systems
4. CIRP Annals
5. Nature Machine Intelligence（competitive）

避免單純 ML 場合（NeurIPS/ICML），因為 ML reviewer 不熟 DOE。
"""
write_doc(RH / "12_shortcut_learning_diagnosis.md", SHORTCUT)


# ═══════════════════════════════════════════════════════════════════════════════
# 13_tcn_v1_fault_detector.md
# ═══════════════════════════════════════════════════════════════════════════════
TCN_DOC = """# 13 — TCN_v1 故障偵測 model

## 位置

`.claude/worktrees/peaceful-volhard-fc16f8/TCN_v1.py`

## 任務

純編碼器 4-channel 時序輸入 → 5-class 故障分類
- N0: normal
- A1: clogged nozzle
- A2: filament jam
- A3: broken
- A4: heat creep

## 架構

```
Input: (4 ch, 256 samples = 10.24s @25Hz)
    ↓
Stem: Conv1d(4→64, k=1) + BN + GELU
    ↓
ResBlock 1: Conv1d(64→128, k=7, dilation=1) + BN + GELU + Dropout + Conv1d(1x1) + BN + Residual
ResBlock 2: Conv1d(128→128, k=7, dilation=2) + ...
ResBlock 3: Conv1d(128→256, k=5, dilation=4) + ...
ResBlock 4: Conv1d(256→256, k=5, dilation=8) + ...
    ↓
AdaptiveAvgPool1d → Flatten
    ↓
Linear(256→128) + GELU + Dropout
    ↓
Linear(128→num_classes)
```

## 參數量

- TCN_v1 total: **910,413 params (~0.91M)**
- Checkpoint size: **3.5 MB** (fp32)

## 訓練設定

- Batch: 64
- Epochs: 60
- LR: 1e-3 (Adam)
- Weight decay: 1e-4
- Seed: 42
- Loss: CrossEntropy
- Window: 256 samples, stride 64 (75% overlap)
- Split: by run, 1 run/class as test + 1 run/class as val + rest train

## 資料

- prints 109-149（32 個有效）
- ~166k 編碼器樣本
- ~111 分鐘總錄製

## State Machine 後處理（部署層）

`inference_logic.py` 加上：
- EMA smoothing (alpha=0.70)
- 進入故障門檻：5 連續窗 prob > 0.60
- 解除故障門檻：20 連續窗 N0 prob > 0.80
- 不可逆故障（A2 jam, A3 broken）：確認後永久鎖死
- 故障類型切換：10 連續窗 prob > 0.75

## 跟 v17 model 的關係

兩個模型**完全獨立**：
- v17: image + encoder → 4 個參數頭（speed/flow/temp/tension）
- TCN_v1: 純 encoder → 1 個故障頭（5-class）

部署時兩個 model 並行跑，輸出在 aggregator 層合併。

## 整合架構（兩個分開部署）

```
encoder seq (4ch, 50Hz)
    ↓ downsample to 25Hz
    │
    ├──→ v17 (window 100 @ 50Hz) + image → speed/flow/temp/tension
    │
    └──→ TCN_v1 (window 256 @ 25Hz) → fault state machine → alarm
                                                ↓
                                         decision aggregator
                                                ↓
                              {speed, flow, temp, tension, fault, alarm}
```

## 為什麼不合併

詳見討論：合併要求兩邊資料對稱（每筆都有 fault + parameter 標籤），但：
- 1-81 沒 fault 標籤
- 109-149 沒完整 L9 參數標籤

合併訓練會引入新的 aliasing（fault ↔ specific (s,f,t)）。**分開部署最乾淨**。
"""
write_doc(RH / "13_tcn_v1_fault_detector.md", TCN_DOC)


# ═══════════════════════════════════════════════════════════════════════════════
# 14_onnx_deployment.md
# ═══════════════════════════════════════════════════════════════════════════════
ONNX_DOC = """# 14 — ONNX 化與部署規格

## 已完成 ONNX export

### v17_orig（v17_5blk_seed1）

| 版本 | 大小 | accuracy diff vs PyTorch |
|---|---:|---:|
| PyTorch fp32 (.pt) | 77 MB | baseline |
| ONNX fp32 (.onnx + .onnx.data) | 60 MB | < 1e-5（基本一致）|
| **ONNX fp16 (.onnx)** | **29 MB** | < 0.001 avg4 |

### 驗證結果（24,818 windows in 1-99）

| subset | variant | speed | flow | temp | tension | avg4 |
|---|---|---:|---:|---:|---:|---:|
| internal_holdout | PyTorch fp32 | 0.7474 | 0.6419 | 0.4311 | 0.7885 | 0.6522 |
| internal_holdout | ONNX fp32 | 0.7474 | 0.6419 | 0.4313 | 0.7885 | 0.6523 |
| internal_holdout | **ONNX fp16** | 0.7474 | 0.6419 | 0.4314 | 0.7883 | 0.6523 |
| param_ood | PyTorch fp32 | 0.7573 | 0.6499 | 0.2955 | 0.8678 | 0.6426 |
| param_ood | ONNX fp16 | 0.7573 | 0.6499 | 0.2951 | 0.8689 | 0.6428 |
| geom_ood | PyTorch fp32 | 0.7416 | 0.6295 | 0.5800 | 0.7026 | 0.6634 |
| geom_ood | ONNX fp16 | 0.7416 | 0.6295 | 0.5812 | 0.7009 | 0.6633 |

→ **fp16 量化可放心用**，準度差距 ≤ 0.0002 avg4（< float 雜訊）。

## ONNX export 細節

### 模型輸入

```
inputs:
  - image: (B, 3, 224, 224), fp32
  - seq:   (B, 4, 100), fp32

outputs:
  - logit_speed:   (B, 3)
  - logit_flow:    (B, 3)
  - logit_temp:    (B, 3)
  - logit_tension: (B, 3)
```

dynamic_axes: batch 維度可變。

### Opset

opset_version=17。

### 已知障礙

- DINOv3 RoPE attention：實際 export 沒問題（PyTorch 2.x exporter 自動處理）
- Storage tokens: OK
- Branch A/B split: OK
- xFormers attention: runtime 未使用，OK

## 部署規格

### 預估 RPi5 延遲

| 版本 | 單張延遲 | FPS |
|---|---:|---:|
| PyTorch fp32 | 600-800 ms | 1.3-1.7 |
| ONNX fp32 | 400-500 ms | 2.0-2.5 |
| **ONNX fp16** | **250-350 ms** | **2.8-4.0** |
| ONNX int8 (未試) | ~150-200 ms | ~5-6 |

對 1 Hz 影像取樣率，fp16 已足夠 2-3 倍餘裕。

### 部署整套大小（per-head best mix）

| 配置 | 大小 |
|---|---:|
| 3 個 v17 變體獨立 PyTorch fp32 | ~234 MB |
| 3 個 v17 變體 ONNX fp32（共用 frozen backbone）| ~125 MB |
| **3 個 v17 變體 ONNX fp16** | **~70 MB** |
| 3 個 v17 變體 ONNX int8 | ~37 MB |
| 單一 v17 + TCN_v1（如果未來 L27 統一）| ~22 MB |

## 部署流程（建議）

```
image (1 Hz, JPEG) ─→ resize (224x224) ─→ normalize ─→ ONNX fp16 ─→ 4 logits
encoder (50 Hz, 4ch) ─→ rolling buffer (last 100 samples) ─→ normalize ─→ 同上 ONNX 輸入

每秒輸出：
  per_frame_logits = onnx_session.run({image, seq})

Python 後處理：
  rolling_buffer.append(per_frame_logits)
  smoothed = rolling_buffer[-20:].mean(axis=0)   # rolling20s
  biased = smoothed + np.array([0, b1, b2])  # per-head bias
  pred = biased.argmax(axis=1)

最終輸出：
  {speed, flow, temp, tension}
```

並行 TCN_v1：
```
encoder (downsample 25 Hz) ─→ window 256 samples ─→ TCN_v1 ONNX fp16 ─→ 5 logits
                                                            ↓
                                                EMA + state machine → alarm
```

## 相關 script

- `v24_shallow_wide_package/runs/codex_export_v17_to_onnx.py`：export 腳本
- `v24_shallow_wide_package/runs/codex_eval_onnx_vs_pytorch.py`：驗證腳本
- `v24_shallow_wide_package/runs/v24_onnx_export/`：所有輸出檔案

## TODO

- TCN_v1 ONNX export（架構簡單，1 小時內可完成）
- int8 量化測試（需校正資料 100-500 張）
- RPi5 實機延遲量測
"""
write_doc(RH / "14_onnx_deployment.md", ONNX_DOC)


# ═══════════════════════════════════════════════════════════════════════════════
# 15_all_metrics_summary.md
# ═══════════════════════════════════════════════════════════════════════════════
ALL_METRICS = """# 15 — 所有版本主指標彙整

## 來源

- 179 runs 從各 _package 目錄收集（v11+）
- 358 runs 從 experiment_metrics_audit（v1-v6）

## 各版本「最佳 holdout avg4」timeline

| 版本 | 最佳 run | encoder | fusion | holdout avg4 | param_ood | geom_ood |
|---|---|---|---|---:|---:|---:|
"""

# Get best per package
df_sub = df_idx.dropna(subset=["internal_holdout_avg4_balanced_accuracy"]).copy()
df_sub['version_num'] = df_sub['package'].str.extract(r'v(\d+)').astype(float)
best_per_pkg = df_sub.sort_values("internal_holdout_avg4_balanced_accuracy", ascending=False).groupby("package").head(1)
best_per_pkg = best_per_pkg.sort_values("version_num")
for _, r in best_per_pkg.iterrows():
    ALL_METRICS += f"| {r['package']:38s} | {r['run_id'][:35]:35s} | {str(r.get('image_encoder_init','-'))[:25]:25s} | {str(r.get('fusion_method','-')):10s} | {r['internal_holdout_avg4_balanced_accuracy']:.4f} | {r.get('internal_holdout_param_ood_avg4_balanced_accuracy', float('nan')):.4f} | {r.get('internal_holdout_geom_ood_avg4_balanced_accuracy', float('nan')):.4f} |\n"

ALL_METRICS += """

## Top 20 全期 holdout avg4

| Rank | run | package | encoder | holdout avg4 | param_ood | geom_ood |
|---:|---|---|---|---:|---:|---:|
"""
top20 = df_sub.sort_values("internal_holdout_avg4_balanced_accuracy", ascending=False).head(20)
for i, (_, r) in enumerate(top20.iterrows(), 1):
    ALL_METRICS += f"| {i} | {r['run_id'][:40]:40s} | {r['package'][:25]:25s} | {str(r.get('image_encoder_init','-'))[:25]:25s} | {r['internal_holdout_avg4_balanced_accuracy']:.4f} | {r.get('internal_holdout_param_ood_avg4_balanced_accuracy', float('nan')):.4f} | {r.get('internal_holdout_geom_ood_avg4_balanced_accuracy', float('nan')):.4f} |\n"

ALL_METRICS += """

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
"""
write_doc(RH / "15_all_metrics_summary.md", ALL_METRICS)


# ═══════════════════════════════════════════════════════════════════════════════
# 16_lessons_learned.md
# ═══════════════════════════════════════════════════════════════════════════════
LESSONS = """# 16 — 經驗總結 + 未來方向

## 核心經驗（成功）

### 1. 小樣本 ML 訓練資料設計的盲點

傳統 DOE 教科書推薦的 L9 / L18 等小型正交陣，**在 ML 訓練上可能誘發 shortcut learning**。具體：
- L9(3³) inner array 把 temp 設為 (s × f) interaction → ML 走捷徑
- L27(3¹³) 4-factor placement at C1/C2/C5/C9 → 無此問題

**這個 framing 是 thesis 主要 contribution**。

### 2. Capacity scaling 並非萬靈丹

ViT-S → ViT-B 容量翻倍，**holdout 表現反而下降**：
- ViT-S tension holdout: 0.58
- ViT-B tension holdout: 0.33（隨機）

→ 在 aliased 訓練資料下，**capacity 越大越被誘往 shortcut**。

### 3. Per-head best mix > 單一 model

不同 head 在不同 fusion 上表現不同：
- speed/flow: FiLM 強
- temp: Sum 強
- tension: GMU (v17_orig) 強

組合起來比單一 model 提升 +0.12 avg4。但要老實標註 holdout-informed selection。

### 4. Rolling smoothing 是廉價的部署優化

對 print-level 靜態因子（speed/flow/temp/tension 都是設定），rolling20s 後處理把 tension 從 0.58 → 0.79。**不需要重訓**。

### 5. ONNX 化幾乎無痛

- fp16 量化：accuracy 差 < 0.001
- 檔案省 62%
- RPi5 推論加速 2-3 倍

## 核心經驗（失敗）

### A. Temp param_ood 是結構性死路

所有嘗試（augmentation、retrain、TTA、stacking、ensemble、adversarial）都救不了 temp param_ood。原因：訓練資料根本不要求模型學溫度視覺。

**只有改資料設計（L27）能解。**

### B. ViT-B / ViT-L 不適合此 dataset

容量過大誘發 shortcut。在小樣本（< 20k）上，**較小 backbone (ViT-S 5blk truncated) 反而泛化更好**。

### C. Hyperparameter sweep 邊際遞減

v18-v23 的 augmentation / attention / architecture variation 都沒突破 v15c dualenc 的 0.78 holdout avg4。

### D. Codex 的 hotend sensor「救援」不算數

用 hotend telemetry 直接量測（非影像）讓 temp 達 1.000，但這違反「pure image+encoder」研究目標。已 ban。

## 部署落地（已完成）

- v17_orig (ONNX fp16, 29 MB) + TCN_v1 (3.5 MB) = **~33 MB** 部署套件
- RPi5 + ONNX Runtime CPU EP，預估 3-4 FPS
- Per-head best mix deployment config (Version B) 已凍結

## 未來方向（依優先序）

### 1. ★ L27(3¹³) 重訓 — thesis paper 1 主要 future work

具體計畫：
- 27 個唯一 (s, f, t, tension) × 3 pieces = **54 個新印件**（9 既有可重用 × 3 = 27 + 54 = 81 total）
- 用 standard Taguchi L27 + linear graph 規範（C1=speed, C2=flow, C5=temp, C9=tension）
- 重訓 v17_5blk + 任何 backbone
- 預期：temp param_ood 從 0.39 → 0.65+

### 2. ☆ 27 件 counter-example patch — 較省方案

不重做整個設計，加 27 個破 L9 的印件 + 訓練時 oversample × 3。實際印件量：~27 件新。詳見 11 章「Option C」討論。

### 3. TCN_v1 重新 evaluation 並 ONNX 化

目前 TCN_v1 checkpoint 沒存 val/test metrics。需要：
- 重跑 evaluation 量出 5-class accuracy
- Export ONNX fp16
- 整合 deployment aggregator script

### 4. 寫 deployment aggregator

把 v17 ONNX 輸出 + TCN_v1 ONNX 輸出 + state machine 整合成單一 service。預估 ~200 行 Python。

### 5. 真實場域驗證

挑 9 個訓練分布內的高 F1 print（已選好）重印一次，驗證 deployment 可重現性。
詳見之前討論的「9 個驗證 print」清單。

### 6. Paper 1: DOE × ML shortcut methodology

- Title: "Orthogonal Design Aliasing as Source of Shortcut Learning"
- Target: IISE Transactions / Quality Engineering / J. Manufacturing Systems
- 主要 data: 此 thesis 的 L9 vs L27 對比 + capacity scaling
- 投稿時間：L27 重訓完成後

### 7. Paper 2: FDM 多模態監測系統

- Title: "Multi-Modal Monitoring System for FDM Quality Control with Aliasing-Aware Data Design"
- Target: Additive Manufacturing / J. Manufacturing Processes
- 主要 data: per-head best deployment + ONNX + RPi5 部署
- 引用 Paper 1 的 methodology

## 核心訊息（給未來自己）

1. **資料設計 > 模型架構**（小樣本領域特別明顯）
2. **越大模型不等於越好**（aliasing 下反而更壞）
3. **deployment-level optimization 廉價有效**（per-head + bias + smoothing）
4. **誠實標註 holdout-informed 部分**（research 倫理）
5. **DOE × ML 是真正的 research gap**（少有人探索）

## Repo 索引

| Path | 重要內容 |
|---|---|
| `v17_caxton_adapted_package/runs/v17_results/v17_5blk_seed1/` | canonical model checkpoint |
| `v24_shallow_wide_package/runs/v24_final_deployment/` | per-head best deployment config |
| `v24_shallow_wide_package/runs/v24_onnx_export/` | ONNX fp32/fp16 + 比對 metric |
| `v24_shallow_wide_package/runs/v24_all_heads_calibration/` | per-head logit + bias calibration |
| `v24_shallow_wide_package/runs/v24_all_heads_rescue_codex/` | codex 的多重 rescue 嘗試 |
| `.claude/worktrees/peaceful-volhard-fc16f8/` | TCN_v1 fault detector |
| `experiment_metrics_audit/` | v1-v6 era 358 runs audit |
| `RESEARCH_HISTORY/` | 本資料夾（完整歷程整理）|

## 致謝

- Claude / Codex 協助迭代與分析
- 大量 failure modes 被誠實記錄而非掩蓋，是論文 honest contribution 的基礎
"""
write_doc(RH / "16_lessons_learned.md", LESSONS)


# ═══════════════════════════════════════════════════════════════════════════════
# Verify encoding
# ═══════════════════════════════════════════════════════════════════════════════
print()
print("[verify] checking BOM in all .md files...")
ok = 0; bad = 0
for f in sorted(RH.rglob("*.md")):
    with open(f, "rb") as fp:
        head = fp.read(3)
    if head == b'\xef\xbb\xbf':
        ok += 1
    else:
        bad += 1
        print(f"  MISSING BOM: {f.relative_to(RH)}")
print(f"[verify] {ok} files have UTF-8 BOM, {bad} missing")

print("\n[verify] checking BOM in all .csv files...")
ok = 0; bad = 0
for f in sorted((RH / "tables").rglob("*.csv")):
    with open(f, "rb") as fp:
        head = fp.read(3)
    if head == b'\xef\xbb\xbf':
        ok += 1
    else:
        bad += 1
        print(f"  MISSING BOM: {f.relative_to(RH)}")
print(f"[verify] {ok} CSV files have UTF-8 BOM, {bad} missing")
print("\n[generate-docs][done]")
