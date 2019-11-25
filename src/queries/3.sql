WITH Recent_appointment AS(
SELECT client_id, CAST(DATE_PART('day', appointment_date) - 1 as int) / 7 as week_num
FROM Appointment
WHERE DATE_PART('month',appointment_date) = DATE_PART('month',CURRENT_DATE - interval '1 month')),

Appointment_each_week AS(
SELECT client_id, week_num, count(Recent_appointment)
FROM Recent_appointment
GROUP BY client_id, week_num
HAVING COUNT(Recent_appointment) >= 2)

select Client.name
from Appointment_each_week JOIN Client on client_id = Client.id
GROUP BY Client.name
HAVING COUNT(Client.id) >= 4

where visits1 >= 2 and visits2 >= 2 and visits3 >= 2 and visits4 >= 2;