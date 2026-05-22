# 12 — 核心研究發現：DOE Aliasing → ML Shortcut Learning

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
