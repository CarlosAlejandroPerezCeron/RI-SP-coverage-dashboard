import os
import matplotlib.pyplot as plt
from utils import get_env, log

def export_dashboard(df):
    out = get_env("OUTPUT_DIR", "./reports")
    os.makedirs(out, exist_ok=True)

    summary = df.groupby("type")[["utilization", "gap"]].mean().round(2)
    summary.to_csv(os.path.join(out, "dashboard_summary.csv"))
    log("Summary exported.")

    plt.figure(figsize=(8,5))
    plt.bar(df["type"], df["utilization"], color=["#1f77b4", "#ff7f0e"])
    plt.axhline(y=float(get_env("TARGET_COVERAGE")), color="r", linestyle="--", label="Target")
    plt.title("RI/SP Utilization vs Target")
    plt.ylabel("Utilization %")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out, "coverage_chart.png"))
    log("Coverage chart saved.")
