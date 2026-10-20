INSERT INTO rep.market_share_report (date_time, city_id, qty_share, amt_share)
WITH competition AS (
    SELECT date_id::date AS report_date, city_id,
           sum(sales_qty) AS total_qty, sum(sales_amt) AS total_amt
    FROM cdm.f_customer_research
    GROUP BY date_id::date, city_id
), ours AS (
    SELECT create_date AS report_date, city_id,
           sum(quantity) AS total_qty, sum(payment_amount) AS total_amt
    FROM cdm.f_order
    GROUP BY create_date, city_id
)
SELECT o.report_date, o.city_id,
       o.total_qty::numeric / NULLIF(o.total_qty + c.total_qty, 0),
       o.total_amt::numeric / NULLIF(o.total_amt + c.total_amt, 0)
FROM ours o
JOIN competition c ON o.report_date = c.report_date AND o.city_id = c.city_id
ON CONFLICT (date_time, city_id) DO UPDATE
SET qty_share = EXCLUDED.qty_share, amt_share = EXCLUDED.amt_share;
