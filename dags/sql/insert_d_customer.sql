begin transaction;

INSERT INTO cdm.d_customer(customer_id, first_name, last_name, start_date, end_date)
SELECT stg.customer_id,
       stg.first_name,
       stg.last_name,
       '{{ ds }}'::date,
       '9999-12-31'::date
FROM stg.d_customer stg;

UPDATE cdm.d_customer
set end_date = '{{ ds }}'::date - interval '1 day'
WHERE id IN (SELECT id
             FROM stg.d_customer
             WHERE id IS NOT NULL);

INSERT INTO cdm.d_customer(customer_id, first_name, last_name, start_date, end_date)
SELECT DISTINCT uol.customer_id,
                'неизвестно',
                'неизвестно',
                '{{ ds }}'::date,
                '9999-12-31'::date
FROM ods.user_activity_log uol
         LEFT JOIN cdm.d_customer dim USING (customer_id)
WHERE dim.id IS NULL;

commit transaction;
