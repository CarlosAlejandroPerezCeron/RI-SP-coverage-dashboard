import boto3
import pandas as pd
from utils import get_env, log

def fetch_ri_data():
    client = boto3.client("ce", region_name=get_env("AWS_REGION"))
    response = client.get_reservation_utilization(
        TimePeriod={"Start": "2025-12-01", "End": "2025-12-31"},
        Granularity="MONTHLY"
    )

    records = []
    for item in response["UtilizationsByTime"]:
        for group in item["Groups"]:
            records.append({
                "family": group["Attributes"].get("InstanceTypeFamily", "Unknown"),
                "region": group["Attributes"].get("Region", "Unknown"),
                "utilization": float(group["Utilization"]["UtilizationPercentage"]),
                "coverage": float(group["Utilization"]["PurchasedHours"]),
                "date": item["TimePeriod"]["Start"]
            })

    df = pd.DataFrame(records)
    log(f"Fetched {len(df)} RI records.")
    return df
