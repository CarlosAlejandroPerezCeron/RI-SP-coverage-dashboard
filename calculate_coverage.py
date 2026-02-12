import pandas as pd
from utils import get_env, log

def calculate_coverage(ri_df, sp_df):
    target = float(get_env("TARGET_COVERAGE", 85))

    ri_df["type"] = "RI"
    sp_df["type"] = "SP"
    combined = pd.concat([ri_df, sp_df], ignore_index=True)

    combined["meets_target"] = combined["utilization"] >= target
    combined["gap"] = target - combined["utilization"]
    combined["gap"] = combined["gap"].apply(lambda x: 0 if x < 0 else x)

    log("Coverage calculation complete.")
    return combined
