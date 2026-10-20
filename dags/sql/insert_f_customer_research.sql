INSERT INTO cdm.f_customer_research (date_id, category_id, city_id, sales_qty, sales_amt)
SELECT r.date_id, r.category_id, c.id, r.sales_qty, r.sales_amt
FROM ods.customer_research r
JOIN cdm.d_city c ON c.city_id = r.geo_id
    AND r.date_id::date BETWEEN c.start_date AND c.end_date
WHERE r.date_id::date = '{{ ds }}'::date
ON CONFLICT (date_id, category_id, city_id) DO UPDATE
SET sales_qty = EXCLUDED.sales_qty, sales_amt = EXCLUDED.sales_amt;
