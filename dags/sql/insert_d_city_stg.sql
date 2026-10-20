WITH
     api_data AS ( --актуальные на дату расчёта данные в источнике
         SELECT DISTINCT
         ON (uol.city_id)
             uol.city_id,
             uol.city_name
         FROM ods.user_order_log uol
         WHERE
             uol.date_time::date = '{{ ds }}'::date
         ORDER BY uol.city_id, date_time DESC
)
INSERT INTO stg.d_city (id, city_id, city_name)
SELECT --получаем дельту и вставляем данные
       dim.id,
       uol.city_id,
       uol.city_name
FROM api_data uol
         LEFT JOIN cdm.d_city dim on dim.city_id = uol.city_id
         and '{{ ds }}'::date BETWEEN start_date AND end_date
WHERE (uol.city_name != dim.city_name and dim.end_date = '9999-12-31'::date)
  OR dim.city_id IS NULL;
