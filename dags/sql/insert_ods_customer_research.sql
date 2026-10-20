INSERT INTO ods.customer_research (date_id, category_id, geo_id, sales_qty, sales_amt)
SELECT date_id, category_id, geo_id, max(sales_qty), max(sales_amt)
FROM raw.customer_research
WHERE date_id::date = '{{ ds }}'::date
GROUP BY date_id, category_id, geo_id
ON CONFLICT (date_id, category_id, geo_id) DO UPDATE
SET sales_qty = EXCLUDED.sales_qty, sales_amt = EXCLUDED.sales_amt;
