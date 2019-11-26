WITH visits_on_last_month AS

(SELECT name, count(name) AS visits, age
FROM Client AS c INNER JOIN Appointment AS a ON c.id = a.client_id
WHERE DATE_PART('month',appointment_date) = DATE_PART('month',CURRENT_DATE - interval '1 month')
GROUP BY c.name, c.age)

SELECT sum
(
CASE
WHEN visits < 3 AND age < 50 THEN visits*200
WHEN visits < 3 AND age >= 50 THEN visits*400
WHEN visits >= 3 AND age < 50 THEN visits*250
WHEN visits >=3 AND age >= 50 THEN visits*500
END
) AS Income
FROM visits_on_last_month;
