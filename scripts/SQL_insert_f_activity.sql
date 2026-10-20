INSERT INTO cdm.f_activity (activity_id, create_date, customer_id, action_id, quantity)
SELECT uniq_id         AS activity_id,
       date_time::date AS create_date,
       cus.id      AS customer_id,
       ual.action_id      ,
       quantity
FROM ods.user_activity_log ual
         JOIN cdm.d_customer cus ON cus.customer_id = ual.customer_id and '{{ ds }}'::date BETWEEN cus.start_date AND cus.end_date
         WHERE ual.date_time::date = '{{ ds }}'::date
on conflict(activity_id) do NOTHING;
