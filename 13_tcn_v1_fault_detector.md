# 13 — TCN_v1 故障偵測 model

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
