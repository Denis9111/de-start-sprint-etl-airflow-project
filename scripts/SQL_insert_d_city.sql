begin transaction;

INSERT INTO cdm.d_city(city_id, city_name, start_date, end_date)
SELECT stg.city_id,
       stg.city_name,
       '{{ ds }}'::date,
       '9999-12-31'::date
FROM stg.d_city stg;

UPDATE cdm.d_city
set end_date = '{{ ds }}'::date - interval '1 day'
WHERE id IN (SELECT id
             FROM stg.d_city
             WHERE id IS NOT NULL);

commit transaction;
