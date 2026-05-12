SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers_count,
    SUM(o.revenue) AS revenue,
    SUM(o.margin) AS margin,
    AVG(s.score) AS avg_satisfaction
FROM customers_clean c
LEFT JOIN orders_clean o
    ON c.customer_id = o.customer_id
LEFT JOIN satisfaction_clean s
    ON c.customer_id = s.customer_id
GROUP BY c.segment
ORDER BY revenue DESC;