begin transaction;
INSERT INTO cdm.d_item(item_id, item_name, start_date, end_date)
SELECT stg.item_id,
       stg.item_name,
       '{{ ds }}'::date,
       '9999-12-31'::date
FROM stg.d_item stg;

UPDATE cdm.d_item
set end_date = '{{ ds }}'::date - interval '1 day'
WHERE id IN (SELECT id
             FROM stg.d_item
             WHERE id IS NOT NULL);

commit transaction;
