WITH
     api_data AS ( --актуальные на дату расчёта данные в источнике
         SELECT DISTINCT
         ON (uol.customer_id)
             uol.customer_id,
             uol.first_name,
             uol.last_name
         FROM ods.user_order_log uol
         WHERE
             uol.date_time::date = '{{ ds }}'::date
         ORDER BY uol.customer_id, date_time DESC
)
INSERT INTO stg.d_customer (id, customer_id, first_name, last_name)
SELECT --получаем дельту и вставляем данные
       dim.id,
       uol.customer_id,
       uol.first_name,
       uol.last_name
FROM api_data uol
LEFT JOIN cdm.d_customer dim ON dim.customer_id = uol.customer_id AND '{{ ds }}'::date BETWEEN start_date AND end_date
WHERE ((uol.first_name != dim.first_name OR uol.last_name != dim.last_name) and dim.end_date = '9999-12-31'::date)
   OR dim.customer_id IS NULL;
