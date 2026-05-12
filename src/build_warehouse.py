import duckdb
import pandas as pd
import os

DB_PATH = "data/processed/pulse360.duckdb"


def build_warehouse(demo_folder="kultura"):
    os.makedirs("data/processed", exist_ok=True)

    data_path = f"data/demo/{demo_folder}"

    customers = pd.read_csv(f"{data_path}/customers.csv")
    orders = pd.read_csv(f"{data_path}/orders.csv")
    marketing = pd.read_csv(f"{data_path}/marketing_spend.csv")
    satisfaction = pd.read_csv(f"{data_path}/satisfaction.csv")
    events = pd.read_csv(f"{data_path}/events.csv")

    con = duckdb.connect(DB_PATH)

    tables = [
        "customers",
        "orders",
        "marketing_spend",
        "satisfaction",
        "events",
    ]

    for table in tables:
        con.execute(f"DROP TABLE IF EXISTS {table}")

    con.register("customers_df", customers)
    con.register("orders_df", orders)
    con.register("marketing_df", marketing)
    con.register("satisfaction_df", satisfaction)
    con.register("events_df", events)

    con.execute("CREATE TABLE customers AS SELECT * FROM customers_df")
    con.execute("CREATE TABLE orders AS SELECT * FROM orders_df")
    con.execute("CREATE TABLE marketing_spend AS SELECT * FROM marketing_df")
    con.execute("CREATE TABLE satisfaction AS SELECT * FROM satisfaction_df")
    con.execute("CREATE TABLE events AS SELECT * FROM events_df")

    con.close()

    print(f"Warehouse created successfully for demo: {demo_folder}")


if __name__ == "__main__":
    build_warehouse("kultura")