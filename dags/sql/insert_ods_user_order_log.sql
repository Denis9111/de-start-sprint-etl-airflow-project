INSERT INTO ods.user_order_log(id, uniq_id, date_time, city_id, city_name, customer_id, first_name, last_name, item_id,
                               item_name, quantity, payment_amount)
SELECT max(id),
       uniq_id,
       max(date_time),
       max(city_id),
       max(city_name),
       max(customer_id),
       max(first_name),
       max(last_name),
       max(item_id),
       max(item_name),
       max(quantity),
       max(payment_amount)
FROM raw.user_order_log uol
WHERE date_time::date = '{{ ds }}'::date
GROUP BY uniq_id
