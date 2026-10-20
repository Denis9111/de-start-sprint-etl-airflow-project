WITH ours AS (
    SELECT create_date AS report_date, city_id,
           sum(quantity)::numeric AS qty, sum(payment_amount)::numeric AS amt
    FROM cdm.f_order
    WHERE create_date BETWEEN DATE '2024-06-01' AND DATE '2024-12-01'
    GROUP BY create_date, city_id
), competition AS (
    SELECT date_id::date AS report_date, city_id,
           sum(sales_qty)::numeric AS qty, sum(sales_amt)::numeric AS amt
    FROM cdm.f_customer_research
    WHERE date_id::date BETWEEN DATE '2024-06-01' AND DATE '2024-12-01'
    GROUP BY date_id::date, city_id
), expected AS (
    SELECT o.report_date, o.city_id,
           (o.qty / NULLIF(o.qty + c.qty, 0))::double precision AS qty_share,
           (o.amt / NULLIF(o.amt + c.amt, 0))::double precision AS amt_share
    FROM ours o JOIN competition c USING (report_date, city_id)
), actual AS (
    SELECT date_time::date AS report_date, city_id, qty_share, amt_share
    FROM rep.market_share_report
    WHERE date_time::date BETWEEN DATE '2024-06-01' AND DATE '2024-12-01'
)
SELECT COALESCE(e.report_date, a.report_date) AS report_date,
       COALESCE(e.city_id, a.city_id) AS city_id,
       e.qty_share AS expected_qty, a.qty_share AS actual_qty,
       e.amt_share AS expected_amt, a.amt_share AS actual_amt
FROM expected e FULL JOIN actual a USING (report_date, city_id)
WHERE e.report_date IS NULL OR a.report_date IS NULL
   OR e.qty_share IS DISTINCT FROM a.qty_share
   OR e.amt_share IS DISTINCT FROM a.amt_share;
