import pandas as pd


REQUIRED_COLUMNS = {
    "customers": [
        "customer_id", "customer_name", "city", "country", "age_group",
        "segment", "signup_date", "acquisition_channel", "is_member"
    ],
    "orders": [
        "order_id", "customer_id", "order_date", "offer_type",
        "channel", "revenue", "cost", "status"
    ],
    "marketing_spend": [
        "month", "channel", "spend", "impressions", "clicks", "conversions"
    ],
    "satisfaction": [
        "feedback_id", "customer_id", "date", "score",
        "complaint_category", "comment"
    ],
    "events": [
        "event_id", "event_date", "event_type", "city",
        "capacity", "tickets_sold", "revenue", "cost"
    ],
}


def validate_dataframe(df: pd.DataFrame, table_name: str) -> dict:
    expected = REQUIRED_COLUMNS[table_name]
    missing_columns = [col for col in expected if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in expected]

    return {
        "table": table_name,
        "is_valid": len(missing_columns) == 0,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def validate_csv(path: str, table_name: str) -> dict:
    df = pd.read_csv(path)
    return validate_dataframe(df, table_name)