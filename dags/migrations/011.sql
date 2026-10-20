CREATE TABLE rep.market_share_report (
    date_time TIMESTAMP NOT NULL,
    city_id BIGINT NOT NULL,
    qty_share DOUBLE PRECISION,
    amt_share DOUBLE PRECISION,
    CONSTRAINT market_share_report_uniq UNIQUE (date_time, city_id)
);
