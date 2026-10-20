CREATE TABLE ods.customer_research (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_id TIMESTAMP NOT NULL,
    category_id BIGINT NOT NULL,
    geo_id BIGINT NOT NULL,
    sales_qty BIGINT,
    sales_amt BIGINT,
    CONSTRAINT customer_research_unique_key UNIQUE (date_id, category_id, geo_id)
);
