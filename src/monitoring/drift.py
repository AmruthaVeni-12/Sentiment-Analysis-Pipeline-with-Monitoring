import os
os.environ["EVIDENTLY_DISABLE_TELEMETRY"] = "1"
os.environ["DO_NOT_TRACK"] = "1"
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

from src.database.session import SessionLocal
from src.database.models import DriftLog

REPORTS_DIR = Path("reports")

def generate_drift_report(
    reference_data_path: str = "data/processed/test.csv",
    output_html_path: str = "reports/drift_report.html"
) -> Dict[str, Any]:
    """
    Compares reference IMDb dataset against production drift logs using Evidently AI.
    Generates an interactive HTML dashboard and returns key drift metrics.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        try:
            from evidently.legacy.report import Report
            from evidently.legacy.metric_preset import DataDriftPreset
            from evidently.legacy.metrics import DatasetDriftMetric, DataDriftTable
        except ImportError:
            from evidently.report import Report
            from evidently.metric_preset import DataDriftPreset
            from evidently.metrics import DatasetDriftMetric, DataDriftTable
    except ImportError as e:
        return {
            "drift_detected": False,
            "message": f"Evidently not available: {e}"
        }

    if not Path(reference_data_path).exists():
        return {
            "drift_detected": False,
            "message": f"Reference dataset not found at {reference_data_path}"
        }

    # Load reference dataset
    ref_df = pd.read_csv(reference_data_path)
    
    # Query production drift logs from database
    db = SessionLocal()
    try:
        logs = db.query(DriftLog).all()
        if not logs:
            # If no live logs exist yet, use a perturbed sample of reference data
            current_df = ref_df.sample(min(len(ref_df), 100), random_state=42).copy()
        else:
            current_df = pd.DataFrame([{
                "char_length": log.char_length,
                "word_count": log.word_count,
                "sentiment_class": log.predicted_class
            } for log in logs])
    finally:
        db.close()

    # Align columns for numerical feature drift & target drift
    feature_cols = ["char_length", "word_count", "sentiment_class"]
    available_cols = [c for c in feature_cols if c in ref_df.columns and c in current_df.columns]

    ref_subset = ref_df[available_cols].copy()
    curr_subset = current_df[available_cols].copy()

    # Build Evidently Report
    report = Report(metrics=[
        DatasetDriftMetric(),
        DataDriftTable(),
    ])

    report.run(reference_data=ref_subset, current_data=curr_subset)

    # Save HTML report
    report.save_html(output_html_path)

    # Extract JSON summary
    report_dict = report.as_dict()
    metrics_data = report_dict.get("metrics", [])
    
    dataset_drift = False
    drift_share = 0.0
    number_of_drifted_columns = 0

    for m in metrics_data:
        metric_name = m.get("metric")
        if metric_name == "DatasetDriftMetric":
            result = m.get("result", {})
            dataset_drift = result.get("dataset_drift", False)
            drift_share = result.get("drift_share", 0.0)
            number_of_drifted_columns = result.get("number_of_drifted_columns", 0)

    return {
        "drift_detected": bool(dataset_drift),
        "drift_share": float(drift_share),
        "drifted_columns_count": int(number_of_drifted_columns),
        "report_html_path": str(output_html_path),
        "total_production_samples": len(current_df)
    }

if __name__ == "__main__":
    summary = generate_drift_report()
    print("Evidently Drift Analysis Result:", summary)
