"""Collect run_config_resolved.json + hyperparameter files for each version."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parents[1] / "tables"


def main():
    rows = []
    for p in sorted(ROOT.glob("**/run_config_resolved.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        parts = p.parts
        pkg = None
        for part in parts:
            if part.endswith("_package") or part == "training_pkg_claude":
                pkg = part
                break
        if pkg is None:
            pkg = p.relative_to(ROOT).parts[0]
        row = {
            "package": pkg,
            "run_id": c.get("run_id", p.parent.name),
            "fusion_method": c.get("fusion_method"),
            "image_encoder_init": c.get("image_encoder_init"),
            "regime": c.get("regime"),
            "stage": c.get("stage"),
            "seed": c.get("seed"),
            "source_family": c.get("source_family"),
            "training_mode": c.get("training_mode"),
            "loss_scope": c.get("loss_scope"),
            "architecture_family": c.get("architecture_family"),
            "selection_subset": c.get("selection_subset"),
            "used_internal_holdout_for_selection": c.get("used_internal_holdout_for_selection"),
            "config_path": str(p),
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "all_run_configs.csv", index=False, encoding="utf-8-sig")
    print(f"[configs] collected {len(df)} run configs across {df['package'].nunique()} packages")

    # Also collect hyperparameters files
    hyper_rows = []
    for p in sorted(ROOT.glob("**/v*_hyperparameters.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        parts = p.parts
        pkg = None
        for part in parts:
            if part.endswith("_package"):
                pkg = part
                break
        row = {"package": pkg, "hyperparams_path": str(p)}
        row.update({k: v for k, v in c.items() if not isinstance(v, (list, dict))})
        hyper_rows.append(row)
    if hyper_rows:
        dfh = pd.DataFrame(hyper_rows)
        dfh.to_csv(OUT_DIR / "all_hyperparameters.csv", index=False, encoding="utf-8-sig")
        print(f"[configs] collected {len(dfh)} hyperparameter files")


if __name__ == "__main__":
    main()
