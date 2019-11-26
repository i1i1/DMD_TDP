WITH Recent_appointment AS(
SELECT client_id, CAST(DATE_PART('day', appointment_date) - 1 AS int) / 7 AS week_num
FROM Appointment
WHERE DATE_PART('month',appointment_date) = DATE_PART('month',CURRENT_DATE - interval '1 month')),

Appointment_each_week AS(
SELECT client_id, week_num, count(Recent_appointment)
FROM Recent_appointment
GROUP BY client_id, week_num
HAVING COUNT(Recent_appointment) >= 2)

SELECT Client.name
FROM Appointment_each_week JOIN Client ON client_id = Client.id
GROUP BY Client.name
HAVING COUNT(Client.id) >= 4;