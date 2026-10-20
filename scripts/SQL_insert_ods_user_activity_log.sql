INSERT INTO ods.user_activity_log(id, uniq_id, date_time, action_id, customer_id, quantity)
SELECT max(id),
       uniq_id,
       max(date_time),
       max(action_id),
       max(customer_id),
       max(quantity)
FROM raw.user_activity_log ual
WHERE date_time::date = '{{ ds }}'::date
GROUP BY uniq_id;
