WITH
Appointment_each_year AS(
SELECT doctor_id, COUNT(Appointment) as appointment_count, DATE_PART('year', appointment_date) as year_num
FROM Appointment
WHERE DATE_PART('year', appointment_date) >= DATE_PART('year', CURRENT_date - interval '10 years')
GROUP BY doctor_id, DATE_PART('year', appointment_date)
HAVING COUNT(Appointment) >= 5)

SELECT Employee.name
FROM Employee JOIN Appointment_each_year on Employee.id = doctor_id
GROUP BY name
HAVING COUNT(year_num) >= 10 AND SUM(appointment_count) >= 100