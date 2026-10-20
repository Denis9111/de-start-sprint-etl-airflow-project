-- External city_id=77 intentionally differs from the dimension's surrogate id=1.
INSERT INTO cdm.d_city (id, city_id, city_name, start_date, end_date)
OVERRIDING SYSTEM VALUE VALUES
(1, 77, 'Москва', '2024-01-01', '9999-12-31');

INSERT INTO cdm.d_customer (customer_id, first_name, last_name, start_date, end_date)
VALUES (100, 'Анна', 'Тестовая', '2024-01-01', '9999-12-31');
INSERT INTO cdm.d_item (item_id, item_name, start_date, end_date)
VALUES (100, 'Товар', '2024-01-01', '9999-12-31');
INSERT INTO cdm.f_order (order_id, create_date, customer_id, city_id, item_id,
                         quantity, payment_amount)
SELECT 'market-test', '2024-09-01', c.id, 1, i.id, 9, 7500
FROM cdm.d_customer c CROSS JOIN cdm.d_item i;

INSERT INTO cdm.f_customer_research
    (date_id, category_id, city_id, sales_qty, sales_amt)
VALUES ('2024-09-01', 1001, 1, 11, 5000);
INSERT INTO rep.market_share_report (date_time, city_id, qty_share, amt_share)
VALUES ('2024-09-01', 1, 0.3, 0.35);
