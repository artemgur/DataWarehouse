WITH views_aggregated AS (
    SELECT date_trunc('day', time) AS day, count(*) AS count
    FROM event_view
    GROUP BY day
), clicks_aggregated AS (
    SELECT date_trunc('day', time) AS day, count(*) AS count
    FROM event_store_link_click
    GROUP BY day
)
SELECT views_aggregated.day,
       coalesce(clicks_aggregated.count::decimal, 0) / views_aggregated.count AS conversion_rate
FROM views_aggregated
LEFT JOIN clicks_aggregated ON views_aggregated.day = clicks_aggregated.day
ORDER BY views_aggregated.day;
