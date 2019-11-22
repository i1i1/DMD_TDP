SELECT Employee.name
FROM Client JOIN Appointment ON Client.id = Appointment.client_id
JOIN Employee ON Employee.id = Appointment.doctor_id
WHERE Client.NAME = '%(name)s' AND (Employee.name LIKE 'M%%' OR Employee.name LIKE 'L%%'
OR Employee.name LIKE '%% M%%' OR Employee.name LIKE '%% L%%')
AND NOT(Employee.name LIKE 'M%% M%%' OR Employee.name LIKE 'L%% L%%')
AND appointment_date = (
    SELECT MAX(appointment_date)
    FROM Client JOIN Appointment ON Client.id = Appointment.client_id
    AND name = '%(name)s' );
