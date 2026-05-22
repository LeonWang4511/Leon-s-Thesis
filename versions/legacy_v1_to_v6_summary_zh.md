---
title: v1-v6 中文摘要
nav_order: 11
parent: 版本演進 (Version History)
---
# 所有實驗指標整理

整理範圍：掃描目前 `C:\Users\EM328 Super\Desktop\caxton-new-codex` 內 v1 到 v6 已經產出的 summary/rank/compare 類 CSV。  
注意：這份整理是「現有彙總表審計」，不是重新訓練；v1 早期表格有些只有 primary accuracy，後續 v2+ 主要看四頭 all-head accuracy。

## 輸出檔案

- `C:\Users\EM328 Super\Desktop\caxton-new-codex\experiment_metrics_audit\all_experiment_metrics.csv`：標準化後的完整指標表。
- `C:\Users\EM328 Super\Desktop\caxton-new-codex\experiment_metrics_audit\best_by_version_phase.csv`：每個版本/階段的最佳列。
- `C:\Users\EM328 Super\Desktop\caxton-new-codex\experiment_metrics_audit\best_by_version.csv`：每個版本最佳列。
- `C:\Users\EM328 Super\Desktop\caxton-new-codex\experiment_metrics_audit\top30_overall.csv`：整體 test_mean 前 30。
- `C:\Users\EM328 Super\Desktop\caxton-new-codex\experiment_metrics_audit\top20_strict_or_cv_splits.csv`：只看 LOPO/LOCO/SRPWC 等較嚴格切法的前 20。

## 每版本最佳

| version | phase                    | condition                                                                                                                        | split_policy          | n_runs | train_mean | val_mean | test_mean | test_std | speed_mean | flow_mean | temp_mean | tension_mean |
| ------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------ | ---------- | -------- | --------- | -------- | ---------- | --------- | --------- | ------------ |
| v1      | strict_freeze            | strict_freeze_image_backbone=True                                                                                                |                       |        |            |          | 0.6744    |          | 0.6714     | 0.6563    | 0.6955    |              |
| v2      | piece_cv                 | config_group=fusion_m4_1s                                                                                                        |                       | 3.0    |            |          | 0.7987    | 0.0765   | 0.8148     | 0.7666    | 0.7435    | 0.8698       |
| v3      | window_length_ablation   | window_length=200.0; window_s=4.0                                                                                                |                       | 9.0    |            | 0.4415   | 0.6954    | 0.0587   | 0.7407     | 0.6493    | 0.6266    | 0.7651       |
| v4      | final_leaderboard        | phase=phase1_backbone_ablation; config_name=trial_multimodal_1s; backbone_mode=unfrozen_source; split_policy=leave_one_piece_out | leave_one_piece_out   | 9.0    |            | 0.4599   | 0.6829    | 0.0460   | 0.7522     | 0.6335    | 0.5820    | 0.7638       |
| v5      | ensemble                 | split_policy=leave_one_piece_out                                                                                                 | leave_one_piece_out   |        |            |          | 0.6981    | 0.0294   | 0.7665     | 0.6546    | 0.6313    | 0.7401       |
| v5.1    | top20_conditions         | split_policy=leave_one_piece_out                                                                                                 | leave_one_piece_out   | 6.0    |            | 0.4599   | 0.6915    | 0.0536   | 0.7655     | 0.6309    | 0.6116    | 0.7579       |
| v5.2    | vs_v5_v51                | source=v5_phase3; condition_name=v5_phase3_baseline_raw4; split_policy=leave_one_piece_out                                       | leave_one_piece_out   | 9.0    |            |          | 0.6833    | 0.0459   | 0.7530     | 0.6339    | 0.5828    | 0.7637       |
| v5.3    | nature_vs_strict_splits  | source=v5.3; condition_name=D_smooth4_05s_mask_phase; split_policy=nature_temporal_split                                         | nature_temporal_split | 3.0    |            |          | 0.9545    | 0.0041   |            |           |           |              |
| v6      | phase2_fusion_comparison | fusion_method=gmu                                                                                                                |                       | 12.0   |            |          | 0.6561    | 0.1036   | 0.7234     | 0.6193    | 0.5714    | 0.7103       |

## 整體 Top 15

| version | phase                   | condition                                                                                                          | split_policy          | n_runs | train_mean | val_mean | test_mean | test_std | speed_mean | flow_mean | temp_mean | tension_mean |
| ------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- | ------ | ---------- | -------- | --------- | -------- | ---------- | --------- | --------- | ------------ |
| v5.3    | nature_vs_strict_splits | source=v5.3; condition_name=D_smooth4_05s_mask_phase; split_policy=nature_temporal_split                           | nature_temporal_split | 3.0    |            |          | 0.9545    | 0.0041   |            |           |           |              |
| v5.3    | nature_temporal_split   | condition_name=D_smooth4_05s_mask_phase; feature_config=smooth4_05s_mask_phase; split_policy=nature_temporal_split | nature_temporal_split | 3.0    |            | 0.9850   | 0.9545    | 0.0041   | 0.9539     | 0.9397    | 0.9397    | 0.9848       |
| v5.3    | nature_vs_strict_splits | source=v5.3; condition_name=C_raw2_offset_jitter; split_policy=nature_temporal_split                               | nature_temporal_split | 3.0    |            |          | 0.9538    | 0.0040   |            |           |           |              |
| v5.3    | nature_temporal_split   | condition_name=C_raw2_offset_jitter; feature_config=raw2; split_policy=nature_temporal_split                       | nature_temporal_split | 3.0    |            | 0.9906   | 0.9538    | 0.0040   | 0.9466     | 0.9397    | 0.9390    | 0.9900       |
| v5.3    | nature_vs_strict_splits | source=v5.3; condition_name=A_raw4_baseline; split_policy=nature_temporal_split                                    | nature_temporal_split | 3.0    |            |          | 0.9529    | 0.0035   |            |           |           |              |
| v5.3    | nature_temporal_split   | condition_name=A_raw4_baseline; feature_config=raw4; split_policy=nature_temporal_split                            | nature_temporal_split | 3.0    |            | 0.9851   | 0.9529    | 0.0035   | 0.9470     | 0.9418    | 0.9380    | 0.9848       |
| v5.3    | nature_vs_strict_splits | source=v5.3; condition_name=B_raw2_simple; split_policy=nature_temporal_split                                      | nature_temporal_split | 3.0    |            |          | 0.9505    | 0.0019   |            |           |           |              |
| v5.3    | nature_temporal_split   | condition_name=B_raw2_simple; feature_config=raw2; split_policy=nature_temporal_split                              | nature_temporal_split | 3.0    |            | 0.9879   | 0.9505    | 0.0019   | 0.9414     | 0.9369    | 0.9345    | 0.9889       |
| v2      | piece_cv                | config_group=fusion_m4_1s                                                                                          |                       | 3.0    |            |          | 0.7987    | 0.0765   | 0.8148     | 0.7666    | 0.7435    | 0.8698       |
| v2      | piece_cv                | config_group=trial_multimodal_1s                                                                                   |                       | 3.0    |            |          | 0.7671    | 0.0829   | 0.7982     | 0.7187    | 0.7336    | 0.8180       |
| v2      | piece_cv                | config_group=sample_m2_0p5s                                                                                        |                       | 3.0    |            |          | 0.7636    | 0.0733   | 0.7947     | 0.7173    | 0.7260    | 0.8163       |
| v2      | sampling_gap_ablation   | sample_gap_s=0.5                                                                                                   |                       |        |            |          | 0.7636    | 0.0733   | 0.7947     | 0.7173    | 0.7260    | 0.8163       |
| v2      | piece_cv                | config_group=fusion_m1_1s                                                                                          |                       | 3.0    |            |          | 0.7577    | 0.0839   | 0.7956     | 0.6983    | 0.7157    | 0.8210       |
| v2      | piece_cv                | config_group=sample_m2_1s                                                                                          |                       | 3.0    |            |          | 0.7539    | 0.0750   | 0.7957     | 0.7013    | 0.7168    | 0.8018       |
| v2      | sampling_gap_ablation   | sample_gap_s=1.0                                                                                                   |                       |        |            |          | 0.7539    | 0.0750   | 0.7957     | 0.7013    | 0.7168    | 0.8018       |

## 嚴格或交叉驗證切法 Top 15

| version | phase                   | condition                                                                                                                          | split_policy        | n_runs | train_mean | val_mean | test_mean | test_std | speed_mean | flow_mean | temp_mean | tension_mean |
| ------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------ | ---------- | -------- | --------- | -------- | ---------- | --------- | --------- | ------------ |
| v5      | ensemble                | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out |        |            |          | 0.6981    | 0.0294   | 0.7665     | 0.6546    | 0.6313    | 0.7401       |
| v5.1    | feature_sync_ablation   | suite=targeted_confirm; feature_config=raw2; sync_offset_samples=-6; train_sync_jitter_samples=3; split_policy=leave_one_piece_out | leave_one_piece_out | 6.0    |            | 0.4599   | 0.6915    | 0.0536   | 0.7655     | 0.6309    | 0.6116    | 0.7579       |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4599   | 0.6915    | 0.0536   | 0.7655     | 0.6309    | 0.6116    | 0.7579       |
| v5.1    | targeted_confirmation   | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 12.0   |            | 0.4650   | 0.6902    | 0.0532   | 0.7578     | 0.6309    | 0.6069    | 0.7653       |
| v5.3    | nature_vs_strict_splits | source=v5.1; condition_name=targeted_best_raw2_offset_jitter; split_policy=leave_one_piece_out                                     | leave_one_piece_out | 12.0   |            |          | 0.6902    | 0.0532   |            |           |           |              |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4662   | 0.6894    | 0.0556   | 0.7526     | 0.6330    | 0.6027    | 0.7692       |
| v5.1    | feature_sync_ablation   | suite=combined; feature_config=raw2; sync_offset_samples=-4; train_sync_jitter_samples=3; split_policy=leave_one_piece_out         | leave_one_piece_out | 6.0    |            | 0.4662   | 0.6894    | 0.0556   | 0.7526     | 0.6330    | 0.6027    | 0.7692       |
| v5.1    | feature_sync_ablation   | suite=combined; feature_config=raw2; sync_offset_samples=-6; train_sync_jitter_samples=3; split_policy=leave_one_piece_out         | leave_one_piece_out | 6.0    |            | 0.4700   | 0.6889    | 0.0579   | 0.7500     | 0.6309    | 0.6022    | 0.7727       |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4700   | 0.6889    | 0.0579   | 0.7500     | 0.6309    | 0.6022    | 0.7727       |
| v5.1    | feature_sync_ablation   | suite=combined; feature_config=raw2; sync_offset_samples=-6; train_sync_jitter_samples=0; split_policy=leave_one_piece_out         | leave_one_piece_out | 6.0    |            | 0.4665   | 0.6885    | 0.0579   | 0.7505     | 0.6319    | 0.6041    | 0.7674       |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4665   | 0.6885    | 0.0579   | 0.7505     | 0.6319    | 0.6041    | 0.7674       |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4655   | 0.6883    | 0.0560   | 0.7565     | 0.6237    | 0.6014    | 0.7715       |
| v5.1    | feature_sync_ablation   | suite=combined; feature_config=raw2; sync_offset_samples=0; train_sync_jitter_samples=0; split_policy=leave_one_piece_out          | leave_one_piece_out | 6.0    |            | 0.4655   | 0.6883    | 0.0560   | 0.7565     | 0.6237    | 0.6014    | 0.7715       |
| v5.1    | top20_conditions        | split_policy=leave_one_piece_out                                                                                                   | leave_one_piece_out | 6.0    |            | 0.4651   | 0.6881    | 0.0567   | 0.7563     | 0.6311    | 0.6038    | 0.7610       |
| v5.1    | feature_sync_ablation   | suite=combined; feature_config=raw2; sync_offset_samples=0; train_sync_jitter_samples=3; split_policy=leave_one_piece_out          | leave_one_piece_out | 6.0    |            | 0.4651   | 0.6881    | 0.0567   | 0.7563     | 0.6311    | 0.6038    | 0.7610       |

## 關鍵解讀

1. 最高分整體多來自 `v5.3 nature_temporal_split`，最佳約 `0.9545 +/- 0.0041`。這是 per-print temporal 70/20/10 切法，適合看同一 print 內時序預測，但不能當作最嚴格跨 piece 或跨 combo 泛化。
2. 較嚴格的 piece/combo 類切法裡，早期 v2/v3/v5.1 的 LOPO/piece-CV 大約落在 `0.69~0.80` 區間；LOCO 通常明顯低很多，代表 unseen parameter-combo 泛化仍是最難的。
3. v6 補充實驗確認：TCN window fusion 約 `0.642~0.656`，明顯高於 scalar-current fusion 約 `0.577`；只拿當下 encoder 純量不夠。
4. v6 transfer ablation 顯示 source checkpoint + frozen image backbone 對小資料仍然重要；no-source trainable 在 test 上明顯退步。
5. 所有表格都保留 `source_csv` 欄位，之後可以直接追到原始 summary CSV。
