---
title: v1-v10 早期
nav_order: 1
parent: 版本演進 (Version History)
---
# 02 — 早期版本 v1 - v10 摘要

## 來源

`experiment_metrics_audit/` 整理過 v1-v6 共 358 筆實驗 metric。詳細表格已複製到 `tables/legacy_*.csv`。

## v1-v6 主要進展（從 audit 提取）

依 `legacy_best_by_version.csv`：

| version   | phase                    | condition                                                                                                                        | split_policy          |   n_runs |   train_mean |   val_mean |   test_mean |   test_std |   primary_mean |   speed_mean |   flow_mean |   temp_mean |   tension_mean |   val_test_gap_mean | source_csv                                                                                                                                     | note                                                  |
|:----------|:-------------------------|:---------------------------------------------------------------------------------------------------------------------------------|:----------------------|---------:|-------------:|-----------:|------------:|-----------:|---------------:|-------------:|------------:|------------:|---------------:|--------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------|
| v1        | strict_freeze            | strict_freeze_image_backbone=True                                                                                                | nan                   | nan      |          nan |   nan      |      0.6744 |   nan      |         0.6744 |       0.6714 |      0.6563 |      0.6955 |       nan      |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\新增資料夾\research_package_v1\tables\strict_freeze_comparison.csv                                    | v1 primary_acc based early target run                 |
| v2        | piece_cv                 | config_group=fusion_m4_1s                                                                                                        | nan                   |   3.0000 |          nan |   nan      |      0.7987 |     0.0765 |         0.7750 |       0.8148 |      0.7666 |      0.7435 |         0.8698 |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\v2\research_package_v2\piece_cv_sweeps\piece_cv_20260501_031449\tables\aggregate_by_config.csv   | 3-fold piece CV on corrected tension four-head labels |
| v3        | window_length_ablation   | window_length=200.0; window_s=4.0                                                                                                | nan                   |   9.0000 |          nan |     0.4415 |      0.6954 |     0.0587 |       nan      |       0.7407 |      0.6493 |      0.6266 |         0.7651 |             -0.2540 | C:\Users\EM328 Super\Desktop\caxton-new-codex\v3\research_package_v3\tables\window_length_ablation_aggregate.csv                               | TCN input history length ablation                     |
| v4        | final_leaderboard        | phase=phase1_backbone_ablation; config_name=trial_multimodal_1s; backbone_mode=unfrozen_source; split_policy=leave_one_piece_out | leave_one_piece_out   |   9.0000 |          nan |     0.4599 |      0.6829 |     0.0460 |       nan      |       0.7522 |      0.6335 |      0.5820 |         0.7638 |             -0.2230 | C:\Users\EM328 Super\Desktop\caxton-new-codex\v4\research_package_v4\tables\final_leaderboard.csv                                              | v4 curated leaderboard                                |
| v5        | ensemble                 | split_policy=leave_one_piece_out                                                                                                 | leave_one_piece_out   | nan      |          nan |   nan      |      0.6981 |     0.0294 |       nan      |       0.7665 |      0.6546 |      0.6313 |         0.7401 |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\v5\research_package_v5\tables\phase4_ensemble_summary.csv                                        | v5 ensemble summary                                   |
| v5.1      | top20_conditions         | split_policy=leave_one_piece_out                                                                                                 | leave_one_piece_out   |   6.0000 |          nan |     0.4599 |      0.6915 |     0.0536 |         0.6693 |       0.7655 |      0.6309 |      0.6116 |         0.7579 |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\v5.1\research_package_v5_1\tables\v5_1_top20_conditions.csv                                      | v5.1 top conditions                                   |
| v5.2      | vs_v5_v51                | source=v5_phase3; condition_name=v5_phase3_baseline_raw4; split_policy=leave_one_piece_out                                       | leave_one_piece_out   |   9.0000 |          nan |   nan      |      0.6833 |     0.0459 |       nan      |       0.7530 |      0.6339 |      0.5828 |         0.7637 |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\v5.2\research_package_v5_2\tables\v5_2_vs_v5_v51_summary.csv                                     | v5.2 comparison against v5/v5.1                       |
| v5.3      | nature_vs_strict_splits  | source=v5.3; condition_name=D_smooth4_05s_mask_phase; split_policy=nature_temporal_split                                         | nature_temporal_split |   3.0000 |          nan |   nan      |      0.9545 |     0.0041 |       nan      |     nan      |    nan      |    nan      |       nan      |            nan      | C:\Users\EM328 Super\Desktop\caxton-new-codex\v5.3_nature_split\research_package_v5_3_nature_split\tables\v5_3_nature_vs_lopo_loco_summary.csv | nature split vs strict LOPO/LOCO comparison           |
| v6        | phase2_fusion_comparison | fusion_method=gmu                                                                                                                | nan                   |  12.0000 |          nan |   nan      |      0.6561 |     0.1036 |       nan      |       0.7234 |      0.6193 |      0.5714 |         0.7103 |             -0.1394 | C:\Users\EM328 Super\Desktop\caxton-new-codex\v6\research_package_v6\tables\phase2_combined_rank.csv                                           | causal TCN fusion comparison                          |

## 主要技術演進

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
