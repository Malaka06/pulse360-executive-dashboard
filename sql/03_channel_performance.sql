SELECT
    o.channel,
    SUM(o.revenue) AS revenue,
    SUM(o.margin) AS margin,
    SUM(m.spend) AS marketing_spend,
    SUM(m.conversions) AS conversions,
    SUM(o.revenue) / NULLIF(SUM(m.spend), 0) AS roas,
    SUM(m.spend) / NULLIF(SUM(m.conversions), 0) AS cac
FROM orders_clean o
LEFT JOIN marketing_clean m
    ON o.channel = m.channel
    AND o.order_month = m.month
GROUP BY o.channel
ORDER BY revenue DESC;