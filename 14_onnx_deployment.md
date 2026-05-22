---
title: ONNX 部署
nav_order: 5
---
# 14 — ONNX 化與部署規格

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
