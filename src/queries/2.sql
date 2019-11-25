WITH Appointments_per_time_slot AS
    (SELECT Employee.name, COUNT(Appointment) as num_appointments, DATE_PART('dow', appointment_date) as day_num, appointment_time as time_slot
    FROM Employee JOIN Appointment ON Employee.id = Appointment.doctor_id
    WHERE appointment_date BETWEEN (CURRENT_DATE - interval '1 year') AND CURRENT_DATE
    GROUP BY Employee.name, appointment_date, appointment_time)


SELECT name, SUM(num_appointments), AVG(num_appointments), day_num, time_slot
FROM Appointments_per_time_slot
GROUP BY name, day_num, time_slot
ORDER BY name, day_num, time_slot;


SELECT Employee.name, COUNT(Appointment), DATE_PART('dow', appointment_date), appointment_time
FROM Employee JOIN Appointment ON Employee.id = Appointment.Doctor_id
WHERE appointment_date BETWEEN (CURRENT_DATE - interval '1 year') AND CURRENT_DATE
GROUP BY Employee.name, DATE_PART('dow', appointment_date), appointment_time
/*THIS ONE VVVVVVVV*/
WITH visits_per_time_slot as
(SELECT doctor_id, appointment_date, COUNT(Appointment) as appointment_num, time_slot
FROM Appointment RIGHT OUTER JOIN Time_table ON Appointment.appointment_time = Time_table.time_slot
WHERE appointment_date BETWEEN CURRENT_TIME - interval '1 year' and CURRENT_TIME
GROUP BY doctor_id, appointment_date, COUNT(Appointment), time_slot)

SELECT Employee.name, time_slot, SUM(appointment_num), AVG(appointment_num), DATE_PART('dow', appointment_date)
FROM Employee JOIN visits_per_time_slot ON id = doctor_id
GROUP BY Employee.name, time_slot, DATE_PART('dow', appointment_date); 
/*^^^^^^^^^^^^^^^^*/


