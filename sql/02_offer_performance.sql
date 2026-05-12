SELECT
    offer_type,
    SUM(CASE WHEN is_completed = 1 THEN revenue ELSE 0 END) AS revenue,
    SUM(CASE WHEN is_completed = 1 THEN margin ELSE 0 END) AS margin,
    COUNT(*) AS orders_count,
    AVG(margin_rate) AS avg_margin_rate
FROM orders_clean
GROUP BY offer_type
ORDER BY revenue DESC;