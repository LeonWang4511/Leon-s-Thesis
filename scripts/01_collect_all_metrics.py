"""Survey ALL version packages and extract metrics.json + run_config_resolved.json.

Builds:
  RESEARCH_HISTORY/tables/all_metrics_master.csv   - one row per run, all heads x all subsets
  RESEARCH_HISTORY/tables/all_runs_index.csv       - one row per run, summary
  RESEARCH_HISTORY/tables/version_overview.csv     - one row per version, aggregated
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parents[1] / "tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADS = ["speed", "flow", "temp", "tension"]
SUBSETS = ["train_eval", "id_val", "id_test",
           "internal_holdout", "internal_holdout_param_ood", "internal_holdout_geom_ood",
           "internal_holdout_tension_2"]


def find_all_metrics() -> list[Path]:
    """Find every metrics.json under any *_package or runs/* dir."""
    return sorted(ROOT.glob("**/metrics.json"))


def extract_run(path: Path) -> dict | None:
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(m, dict):
        return None
    if "subsets" not in m:
        return None
    # Walk up path: caxton-new-codex/<pkg>/runs/<stage>/<run_id>/metrics.json
    parts = path.parts
    pkg = None
    for p in parts:
        if p.endswith("_package") or p == "training_pkg_claude":
            pkg = p
            break
    if pkg is None:
        # fallback: try first segment under ROOT
        rel = path.relative_to(ROOT)
        pkg = rel.parts[0]
    row = {
        "package": pkg,
        "run_id": m.get("run_id", path.parent.name),
        "stage": m.get("stage"),
        "fusion_method": m.get("fusion_method"),
        "image_encoder_init": m.get("image_encoder_init"),
        "regime": m.get("regime"),
        "seed": m.get("seed"),
        "selected_epoch": m.get("selected_epoch"),
        "selection_subset": m.get("selection_subset"),
        "used_internal_holdout_for_selection": m.get("used_internal_holdout_for_selection"),
        "elapsed_seconds": m.get("elapsed_seconds"),
        "metrics_path": str(path),
    }
    subs = m.get("subsets", {})
    for sname in SUBSETS:
        sm = subs.get(sname, {})
        ph = sm.get("per_head", {})
        for h in HEADS:
            hd = ph.get(h, {}) if isinstance(ph, dict) else {}
            row[f"{sname}_{h}_balanced_accuracy"] = hd.get("balanced_accuracy_present")
            row[f"{sname}_{h}_accuracy"] = hd.get("accuracy")
            row[f"{sname}_{h}_macro_f1"] = hd.get("macro_f1_present")
        # avg4
        bas = [row.get(f"{sname}_{h}_balanced_accuracy") for h in HEADS]
        if all(b is not None for b in bas):
            row[f"{sname}_avg4_balanced_accuracy"] = sum(bas) / 4
        else:
            row[f"{sname}_avg4_balanced_accuracy"] = None
        # tension legacy fields (when only tension was reported)
        if "tension_balanced_accuracy_present" in sm:
            row[f"{sname}_tension_balanced_accuracy"] = sm["tension_balanced_accuracy_present"]
        if "tension_macro_f1_present" in sm:
            row[f"{sname}_tension_macro_f1"] = sm["tension_macro_f1_present"]
        # all-head accuracy
        if "all_head_accuracy" in sm:
            row[f"{sname}_all_head_accuracy"] = sm["all_head_accuracy"]
    return row


def main():
    print("[collect-metrics] scanning repository...")
    paths = find_all_metrics()
    print(f"[collect-metrics] found {len(paths)} metrics.json files")
    rows = []
    for p in paths:
        r = extract_run(p)
        if r is not None:
            rows.append(r)
    df = pd.DataFrame(rows)
    print(f"[collect-metrics] extracted {len(df)} valid runs")
    print(f"[collect-metrics] packages: {df['package'].nunique()}")
    print(df['package'].value_counts().to_string())
    # Write master metrics
    df.to_csv(OUT_DIR / "all_metrics_master.csv", index=False, encoding="utf-8-sig")
    print(f"[collect-metrics] wrote {OUT_DIR / 'all_metrics_master.csv'}")
    # Slim summary per run
    summary_cols = [
        "package", "run_id", "stage", "fusion_method", "image_encoder_init",
        "regime", "seed", "selected_epoch", "selection_subset",
        "id_val_avg4_balanced_accuracy", "id_test_avg4_balanced_accuracy",
        "internal_holdout_avg4_balanced_accuracy",
        "internal_holdout_param_ood_avg4_balanced_accuracy",
        "internal_holdout_geom_ood_avg4_balanced_accuracy",
        "internal_holdout_tension_balanced_accuracy",
        "internal_holdout_param_ood_tension_balanced_accuracy",
        "internal_holdout_geom_ood_tension_balanced_accuracy",
    ]
    have_cols = [c for c in summary_cols if c in df.columns]
    df[have_cols].to_csv(OUT_DIR / "all_runs_index.csv", index=False, encoding="utf-8-sig")
    # Best per-package
    if "internal_holdout_avg4_balanced_accuracy" in df.columns:
        idx = df.groupby("package")["internal_holdout_avg4_balanced_accuracy"].idxmax()
        idx = idx.dropna()
        if len(idx) > 0:
            best = df.loc[idx.values][have_cols].sort_values(
                "internal_holdout_avg4_balanced_accuracy", ascending=False)
            best.to_csv(OUT_DIR / "best_per_package.csv", index=False, encoding="utf-8-sig")
    print("[collect-metrics][done]")


if __name__ == "__main__":
    main()
