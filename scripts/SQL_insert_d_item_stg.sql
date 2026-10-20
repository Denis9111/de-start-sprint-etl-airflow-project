WITH
     api_data AS ( --актуальные на дату расчёта данные в источнике
         SELECT DISTINCT
         ON (uol.item_id)
             uol.item_id,
             uol.item_name
         FROM ods.user_order_log uol
         WHERE
             uol.date_time::date = '{{ ds }}'::date
         ORDER BY uol.item_id, date_time DESC
)
INSERT INTO stg.d_item (id, item_id, item_name)
SELECT --получаем дельту и вставляем данные
       dim.id,
       uol.item_id,
       uol.item_name
FROM api_data uol
         LEFT join cdm.d_item dim on dim.item_id = uol.item_id
         and '{{ ds }}'::date BETWEEN dim.start_date AND dim.end_date
WHERE (uol.item_name != dim.item_name and dim.end_date = '9999-12-31'::date)
   OR dim.item_id IS NULL;
