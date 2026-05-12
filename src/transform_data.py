import duckdb
import os

DB_PATH = "data/processed/pulse360.duckdb"


def run_transformations():
    os.makedirs("data/processed", exist_ok=True)
    con = duckdb.connect(DB_PATH)

    # -----------------------------
    # CLEAN TABLES
    # -----------------------------

    con.execute("""
    CREATE OR REPLACE TABLE orders_clean AS
    SELECT
        order_id,
        customer_id,
        CAST(order_date AS DATE) AS order_date,
        DATE_TRUNC('month', CAST(order_date AS DATE)) AS order_month,
        offer_type,
        channel,
        CAST(revenue AS DOUBLE) AS revenue,
        CAST(cost AS DOUBLE) AS cost,
        CAST(revenue AS DOUBLE) - CAST(cost AS DOUBLE) AS margin,
        CASE 
            WHEN CAST(revenue AS DOUBLE) > 0 
            THEN (CAST(revenue AS DOUBLE) - CAST(cost AS DOUBLE)) / CAST(revenue AS DOUBLE)
            ELSE NULL
        END AS margin_rate,
        status,
        CASE WHEN status = 'Completed' THEN 1 ELSE 0 END AS is_completed,
        CASE WHEN status = 'Refunded' THEN 1 ELSE 0 END AS is_refunded,
        CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END AS is_cancelled
    FROM orders
    """)

    con.execute("""
    CREATE OR REPLACE TABLE customers_clean AS
    SELECT
        customer_id,
        customer_name,
        city,
        country,
        age_group,
        segment,
        CAST(signup_date AS DATE) AS signup_date,
        acquisition_channel,
        CAST(is_member AS INTEGER) AS is_member
    FROM customers
    """)

    con.execute("""
    CREATE OR REPLACE TABLE marketing_clean AS
    SELECT
        CAST(month AS DATE) AS month,
        channel,
        CAST(spend AS DOUBLE) AS spend,
        CAST(impressions AS INTEGER) AS impressions,
        CAST(clicks AS INTEGER) AS clicks,
        CAST(conversions AS INTEGER) AS conversions,
        CASE WHEN impressions > 0 THEN clicks * 1.0 / impressions ELSE NULL END AS ctr,
        CASE WHEN clicks > 0 THEN conversions * 1.0 / clicks ELSE NULL END AS conversion_rate,
        CASE WHEN conversions > 0 THEN spend * 1.0 / conversions ELSE NULL END AS cac
    FROM marketing_spend
    """)

    con.execute("""
    CREATE OR REPLACE TABLE satisfaction_clean AS
    SELECT
        feedback_id,
        customer_id,
        CAST(date AS DATE) AS feedback_date,
        CAST(score AS INTEGER) AS score,
        complaint_category,
        comment,
        CASE 
            WHEN score >= 4 THEN 'Positive'
            WHEN score = 3 THEN 'Neutral'
            ELSE 'Negative'
        END AS sentiment
    FROM satisfaction
    """)

    con.execute("""
    CREATE OR REPLACE TABLE events_clean AS
    SELECT
        event_id,
        CAST(event_date AS DATE) AS event_date,
        DATE_TRUNC('month', CAST(event_date AS DATE)) AS event_month,
        event_type,
        city,
        CAST(capacity AS INTEGER) AS capacity,
        CAST(tickets_sold AS INTEGER) AS tickets_sold,
        CAST(revenue AS DOUBLE) AS revenue,
        CAST(cost AS DOUBLE) AS cost,
        CAST(revenue AS DOUBLE) - CAST(cost AS DOUBLE) AS margin,
        CASE WHEN capacity > 0 THEN tickets_sold * 1.0 / capacity ELSE NULL END AS occupancy_rate
    FROM events
    """)

    # -----------------------------
    # ANALYTICS TABLES
    # -----------------------------

    con.execute("""
    CREATE OR REPLACE TABLE monthly_revenue AS
    SELECT
        order_month AS month,
        SUM(CASE WHEN is_completed = 1 THEN revenue ELSE 0 END) AS revenue,
        SUM(CASE WHEN is_completed = 1 THEN cost ELSE 0 END) AS cost,
        SUM(CASE WHEN is_completed = 1 THEN margin ELSE 0 END) AS margin,
        COUNT(DISTINCT CASE WHEN is_completed = 1 THEN customer_id END) AS active_customers,
        COUNT(*) AS total_orders,
        SUM(is_refunded) AS refunded_orders,
        SUM(is_cancelled) AS cancelled_orders
    FROM orders_clean
    GROUP BY order_month
    ORDER BY order_month
    """)

    con.execute("""
    CREATE OR REPLACE TABLE offer_performance AS
    SELECT
        offer_type,
        SUM(CASE WHEN is_completed = 1 THEN revenue ELSE 0 END) AS revenue,
        SUM(CASE WHEN is_completed = 1 THEN margin ELSE 0 END) AS margin,
        COUNT(*) AS orders_count,
        COUNT(DISTINCT customer_id) AS customers_count,
        AVG(CASE WHEN is_completed = 1 THEN margin_rate ELSE NULL END) AS avg_margin_rate
    FROM orders_clean
    GROUP BY offer_type
    ORDER BY revenue DESC
    """)

    con.execute("""
    CREATE OR REPLACE TABLE channel_performance AS
    SELECT
        o.channel,
        SUM(CASE WHEN o.is_completed = 1 THEN o.revenue ELSE 0 END) AS revenue,
        SUM(CASE WHEN o.is_completed = 1 THEN o.margin ELSE 0 END) AS margin,
        COUNT(DISTINCT o.customer_id) AS customers_count,
        COALESCE(SUM(m.spend), 0) AS marketing_spend,
        COALESCE(SUM(m.conversions), 0) AS conversions,
        CASE 
            WHEN COALESCE(SUM(m.spend), 0) > 0 
            THEN SUM(CASE WHEN o.is_completed = 1 THEN o.revenue ELSE 0 END) / SUM(m.spend)
            ELSE NULL
        END AS roas,
        CASE 
            WHEN COALESCE(SUM(m.conversions), 0) > 0 
            THEN SUM(m.spend) / SUM(m.conversions)
            ELSE NULL
        END AS cac
    FROM orders_clean o
    LEFT JOIN marketing_clean m
        ON o.channel = m.channel
        AND o.order_month = m.month
    GROUP BY o.channel
    ORDER BY revenue DESC
    """)

    con.execute("""
    CREATE OR REPLACE TABLE customer_segments AS
    SELECT
        c.segment,
        COUNT(DISTINCT c.customer_id) AS customers_count,
        SUM(CASE WHEN o.is_completed = 1 THEN o.revenue ELSE 0 END) AS revenue,
        SUM(CASE WHEN o.is_completed = 1 THEN o.margin ELSE 0 END) AS margin,
        AVG(s.score) AS avg_satisfaction
    FROM customers_clean c
    LEFT JOIN orders_clean o
        ON c.customer_id = o.customer_id
    LEFT JOIN satisfaction_clean s
        ON c.customer_id = s.customer_id
    GROUP BY c.segment
    ORDER BY revenue DESC
    """)

    con.close()
    print("Data transformations completed successfully")


if __name__ == "__main__":
    run_transformations()