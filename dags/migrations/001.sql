alter table public.user_order_log
set schema raw;

alter table public.user_activity_log
set schema raw;

/*полностью копируем структуру таблиц*/
CREATE TABLE ods.user_order_log
(
    LIKE raw.user_order_log INCLUDING ALL EXCLUDING IDENTITY
);

CREATE TABLE ods.user_activity_log
(
    LIKE raw.user_activity_log INCLUDING ALL EXCLUDING IDENTITY
);

CREATE TABLE stg.d_customer
(
    id          BIGINT,
    customer_id BIGINT NOT NULL,
    first_name  VARCHAR,
    last_name   VARCHAR
);


CREATE TABLE cdm.d_customer
(
    id          BIGINT generated always AS identity PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    first_name  VARCHAR,
    last_name   VARCHAR NULL,
    start_date  DATE NOT NULL,
    end_date    DATE NOT NULL
);


CREATE TABLE stg.d_item
(
    id        BIGINT,
    item_id   BIGINT NOT NULL,
    item_name VARCHAR
);


CREATE TABLE cdm.d_item
(
    id         BIGINT PRIMARY KEY generated always AS identity,
    item_id    BIGINT NOT NULL,
    item_name  VARCHAR NULL,
    start_date DATE NOT NULL,
    end_date   DATE NOT NULL
);


CREATE TABLE stg.d_city
(
    id        BIGINT,
    city_id   BIGINT NOT NULL,
    city_name VARCHAR
);


CREATE TABLE cdm.d_city
(
    id         BIGINT generated always AS identity PRIMARY KEY,
    city_id    BIGINT NOT NULL,
    city_name  VARCHAR,
    start_date DATE NOT NULL,
    end_date   DATE NOT NULL
);


CREATE TABLE cdm.f_order
(
    id             BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    order_id       VARCHAR NOT NULL UNIQUE,
    create_date    DATE,
    customer_id    BIGINT,
    city_id        BIGINT,
    item_id        BIGINT,
    quantity       BIGINT,
    payment_amount NUMERIC(14, 2),
    CONSTRAINT f_order_pkey PRIMARY KEY (id),
    CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES cdm.d_city (id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES cdm.d_customer (id),
    CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES cdm.d_item (id)
);


CREATE TABLE cdm.f_activity
(
    id             BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
    activity_id    VARCHAR NOT NULL UNIQUE,
    create_date    DATE,
    customer_id    BIGINT,
    action_id      BIGINT,
    quantity       BIGINT,
    CONSTRAINT f_activity_pkey PRIMARY KEY (id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES cdm.d_customer (id)
);


CREATE TABLE rep.customer_report (
    customer_id             BIGINT NOT NULL,
    first_name              VARCHAR,
    last_name               VARCHAR,
    uniq_actions            BIGINT,
    different_actions       BIGINT,
    days_with_actions       INTEGER,
    total_actions           BIGINT,
    uniq_orders             BIGINT,
    days_with_orders        INTEGER,
    cities_visited          BIGINT,
    different_items_bought  BIGINT,
    money_spent             BIGINT
);
CREATE UNIQUE INDEX main_customer ON rep.customer_report USING btree (customer_id);
