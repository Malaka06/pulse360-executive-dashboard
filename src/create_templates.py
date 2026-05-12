import pandas as pd
import os

os.makedirs("data/templates", exist_ok=True)

templates = {
    "customers_template.csv": [
        "customer_id", "customer_name", "city", "country", "age_group",
        "segment", "signup_date", "acquisition_channel", "is_member"
    ],
    "orders_template.csv": [
        "order_id", "customer_id", "order_date", "offer_type",
        "channel", "revenue", "cost", "status"
    ],
    "marketing_spend_template.csv": [
        "month", "channel", "spend", "impressions", "clicks", "conversions"
    ],
    "satisfaction_template.csv": [
        "feedback_id", "customer_id", "date", "score",
        "complaint_category", "comment"
    ],
    "events_template.csv": [
        "event_id", "event_date", "event_type", "city",
        "capacity", "tickets_sold", "revenue", "cost"
    ],
}

for filename, columns in templates.items():
    pd.DataFrame(columns=columns).to_csv(f"data/templates/{filename}", index=False)

print("CSV templates created successfully")