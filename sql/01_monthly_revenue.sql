SELECT
    order_month AS month,
    SUM(CASE WHEN is_completed = 1 THEN revenue ELSE 0 END) AS revenue,
    SUM(CASE WHEN is_completed = 1 THEN cost ELSE 0 END) AS cost,
    SUM(CASE WHEN is_completed = 1 THEN margin ELSE 0 END) AS margin,
    COUNT(DISTINCT CASE WHEN is_completed = 1 THEN customer_id END) AS active_customers
FROM orders_clean
GROUP BY order_month
ORDER BY order_month;