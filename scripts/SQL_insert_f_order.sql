INSERT INTO cdm.f_order (order_id, create_date, customer_id, city_id, item_id, quantity, payment_amount)
SELECT uniq_id         AS order_id,
       date_time::date AS create_date,
       cus.id      AS customer_id,
       c.id         AS city_id,
       it.id        AS item_id,
       quantity,
       payment_amount
FROM ods.user_order_log uol
         JOIN cdm.d_city c on c.city_id = uol.city_id  and '{{ ds }}'::date BETWEEN c.start_date AND c.end_date
         JOIN cdm.d_customer cus ON cus.customer_id = uol.customer_id and '{{ ds }}'::date BETWEEN cus.start_date AND cus.end_date
         JOIN cdm.d_item it on it.item_id = uol.item_id  and '{{ ds }}'::date BETWEEN it.start_date AND it.end_date
WHERE uol.date_time::date = '{{ ds }}'::date
on conflict(order_id) do NOTHING;
