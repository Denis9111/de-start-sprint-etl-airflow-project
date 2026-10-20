CREATE TABLE cdm.f_customer_research (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_id TIMESTAMP NOT NULL,
    category_id BIGINT NOT NULL,
    city_id BIGINT NOT NULL REFERENCES cdm.d_city(id),
    sales_qty BIGINT,
    sales_amt BIGINT,
    CONSTRAINT f_customer_research_unique_key UNIQUE (date_id, category_id, city_id)
);
