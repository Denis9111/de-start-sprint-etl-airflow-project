INSERT INTO rep.customer_report(customer_id ,first_name, last_name, uniq_actions, different_actions,
                            days_with_actions,
                            total_actions, uniq_orders, days_with_orders,
                            cities_visited, different_items_bought, money_spent)
    WITH
         agg_actions AS (SELECT customer_id,
                       COUNT(DISTINCT ual.activity_id)      AS uniq_actions,
                       COUNT(DISTINCT action_id)        AS different_actions,
                       COUNT(DISTINCT ual.create_date)    AS days_with_actions,
                       SUM(ual.quantity)                AS total_actions
                       FROM cdm.f_activity ual
                       GROUP BY customer_id ),
         agg_orders AS (SELECT customer_id,
                   COUNT(DISTINCT uol.order_id)      AS uniq_orders,
                   COUNT(DISTINCT uol.create_date)    AS days_with_orders,
                   COUNT(DISTINCT city_id)          AS cities_visited,
                   COUNT(DISTINCT item_id)          AS different_items_bought,
                   SUM(payment_amount)              AS money_spent
                   FROM cdm.f_order uol
                   GROUP BY customer_id )
    SELECT dc.id ,
           dc.first_name ,
           dc.last_name ,
           uniq_actions,
           different_actions,
           days_with_actions,
           total_actions,
           uniq_orders,
           days_with_orders,
           cities_visited,
           different_items_bought,
           money_spent
    FROM agg_actions ual
             FULL JOIN
         agg_orders uol USING (customer_id)
    JOIN cdm.d_customer dc on dc.id = coalesce(uol.customer_id, ual.customer_id)
     ON CONFLICT (customer_id) DO UPDATE
     SET
     uniq_actions = EXCLUDED.uniq_actions,
     different_actions = EXCLUDED.different_actions,
     days_with_actions = EXCLUDED.days_with_actions,
     total_actions = EXCLUDED.total_actions,
     uniq_orders = EXCLUDED.uniq_orders,
     days_with_orders = EXCLUDED.days_with_orders,
     cities_visited = EXCLUDED.cities_visited,
     different_items_bought = EXCLUDED.different_items_bought,
     money_spent = EXCLUDED.money_spent;
