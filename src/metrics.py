import duckdb

DB_PATH = "data/processed/pulse360.duckdb"


def get_connection():
    return duckdb.connect(DB_PATH)


def get_executive_kpis():
    con = get_connection()

    query = """
    SELECT
        SUM(revenue) AS total_revenue,
        SUM(cost) AS total_cost,
        SUM(margin) AS total_margin,
        COUNT(DISTINCT customer_id) AS active_customers,
        SUM(is_refunded) * 1.0 / COUNT(*) AS refund_rate
    FROM orders_clean
    """

    result = con.execute(query).fetchdf()
    con.close()
    return result


def get_monthly_revenue():
    con = get_connection()
    result = con.execute("SELECT * FROM monthly_revenue ORDER BY month").fetchdf()
    con.close()
    return result


def get_revenue_by_offer():
    con = get_connection()
    result = con.execute("SELECT * FROM offer_performance ORDER BY revenue DESC").fetchdf()
    con.close()
    return result


def get_channel_performance():
    con = get_connection()
    result = con.execute("SELECT * FROM channel_performance ORDER BY revenue DESC").fetchdf()
    con.close()
    return result


def get_customer_segments():
    con = get_connection()
    result = con.execute("SELECT * FROM customer_segments ORDER BY revenue DESC").fetchdf()
    con.close()
    return result