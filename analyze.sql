SELECT COUNT (*) FROM articles;


UPDATE articles
SET date = REPLACE(date, '.', '-');

CREATE VIEW falling AS
  SELECT *
  FROM articles
  WHERE
    title LIKE '%떨어%'
    OR title like '%추락%'
    AND title NOT LIKE '%떨어진%'
    AND title NOT LIKE '%떨어지는%'
;

SELECT COUNT(*) FROM falling;

SELECT title, date FROM articles LIMIT 100;

WITH FIRST_DATE AS (
  SELECT date
  FROM articles
  ORDER BY date ASC
  LIMIT 1
),
LAST_DATE AS (
  SELECT date
  FROM articles
  ORDER BY date DESC
  LIMIT 1
)
SELECT julianday(l.date) - julianday(f.date)
FROM FIRST_DATE f, LAST_DATE l;

CREATE VIEW days_of_reporting AS
  SELECT (julianday(last_date.date) - julianday(first_date.date)) AS days
  FROM
    (SELECT date FROM articles ORDER BY date DESC LIMIT 1) AS last_date,
    (SELECT date FROM articles ORDER BY date ASC LIMIT 1) AS first_date;

SELECT * FROM days_of_reporting;

SELECT r.num_reports / d.days
FROM
  (SELECT COUNT (*) AS num_reports FROM articles) AS r,
  (SELECT days FROM days_of_reporting) AS d;
