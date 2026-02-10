import boto3
import pandas as pd
from utils import get_env, log

def fetch_sp_data():
    client = boto3.client("ce", region_name=get_env("AWS_REGION"))
    response = client.get_savings_plans_utilization_details(
        TimePeriod={"Start": "2025-12-01", "End": "2025-12-31"},
        Granularity="MONTHLY"
    )

    records = []
    for item in response["SavingsPlansUtilizationsByTime"]:
        records.append({
            "sp_arn": item["SavingsPlanArn"],
            "region": item.get("Region", "Global"),
            "coverage": float(item["TotalCommitmentToDate"]),
            "utilization": float(item["UtilizationPercentage"]),
            "date": item["TimePeriod"]["Start"]
        })

    df = pd.DataFrame(records)
    log(f"Fetched {len(df)} SP records.")
    return df
