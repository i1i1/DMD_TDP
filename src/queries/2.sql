WITH days as(
SELECT to_char(generate_series(CURRENT_DATE - interval '1 year', CURRENT_DATE, interval'1 day'), 'day') as day_name,
    DATE_PART('isodow', generate_series(CURRENT_DATE - interval '1 year', CURRENT_DATE, interval'1 day')) as day_num),

Num_week_days as(
SELECT day_name, day_num, count(day_num) as dow_count
FROM days
GROUP BY day_name, day_num),

Doctor_appointments as(
SELECT Employee.name as doctor_name, to_char(appointment_date, 'day') as day_name, appointment_time, COUNT(Appointment) as appointment_count
FROM Employee JOIN Appointment ON Employee.id = Appointment.doctor_id
WHERE appointment_date >= CURRENT_DATE - interval '1 year'
GROUP BY Employee.name, to_char(appointment_date, 'day'), appointment_time
)
SELECT doctor_name, Doctor_appointments.day_name, appointment_time, appointment_count, ROUND(CAST(appointment_count as numeric)/dow_count, 2) as avg_appointments
FROM Doctor_appointments NATURAL JOIN Num_week_days
ORDER BY doctor_name, day_num, appointment_time;