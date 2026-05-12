WITH kpi AS (

SELECT
    SUM(revenue) AS total_revenue,
    SUM(margin) AS total_margin,
    SUM(is_refunded) * 1.0 / COUNT(*) AS refund_rate,
    COUNT(DISTINCT customer_id) AS active_customers
FROM orders_clean

)

SELECT
    total_revenue,
    total_margin,
    refund_rate,
    active_customers,

    (
        ((total_margin / total_revenue) * 100 * 0.45)
        +
        ((1 - refund_rate) * 100 * 0.25)
        +
        ((LEAST(active_customers / 1500.0, 1)) * 100 * 0.30)
    ) AS business_health_score

FROM kpi;