
SELECT Client.name
FROM Client JOIN Appointment ON Client.id = client_id
WHERE appointment_date >= CURRENT_DATE - 


WITH Recent_appointment AS(
SELECT id, DATE_PART('week', appointment_date) as week_num
FROM Appointment
WHERE appoitnment_date >= CURRENT_DATE - interval '1 month';

Appointment_each_week AS
SELECT id, week_num
FROM Recent_appointment
GROUP BY id, week_num
HAVING COUNT(Recent_appointment) >= 2)

SELECT Client.name
FROM Appointment_each_week JOIN Client ON client_id = Client.id
GROUP BY Client.name
HAVING COUNT(Appoitment_each_week) = 4
