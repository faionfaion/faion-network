-- health-score.sql — weekly user health snapshot
-- Each component capped at 25; total range 0-100
-- Retrain thresholds monthly or after major product changes

WITH activity AS (
  SELECT
    user_id,
    COUNT(*) FILTER (WHERE event_date >= CURRENT_DATE - 7)               AS logins_7d,
    COUNT(DISTINCT event_type) FILTER (WHERE event_date >= CURRENT_DATE - 30) AS features_30d,
    MAX(event_date)                                                        AS last_seen
  FROM events
  GROUP BY 1
),
support AS (
  SELECT
    user_id,
    AVG(sentiment_score) AS support_sent
  FROM tickets
  WHERE created_at >= CURRENT_DATE - 60
  GROUP BY 1
)
SELECT
  u.user_id,
  LEAST(25, a.logins_7d * 5)                              AS s_login,
  LEAST(25, a.features_30d * 3)                           AS s_feature,
  COALESCE(s.support_sent, 0.5) * 25                      AS s_support,
  LEAST(25, EXTRACT(DAY FROM AGE(u.signup_date)) / 30)    AS s_tenure,
  (
    LEAST(25, a.logins_7d * 5)
    + LEAST(25, a.features_30d * 3)
    + COALESCE(s.support_sent, 0.5) * 25
    + LEAST(25, EXTRACT(DAY FROM AGE(u.signup_date)) / 30)
  )::int AS health_score
FROM users u
LEFT JOIN activity a USING (user_id)
LEFT JOIN support  s USING (user_id);
