SELECT Employee.name
FROM Client JOIN Appointment ON Client.id = Appointment.client_id
JOIN Employee ON Employee.id = Appointment.doctor_id
WHERE Client.NAME = %name AND (Employee.name LIKE 'M%' OR Employee.name LIKE 'L%'
OR Employee.name LIKE '% M%' OR Employee.name LIKE '% L%')
AND NOT(Employee.name LIKE 'M% M%' OR Employee.name LIKE 'L% L%')
GROUP BY Client.id
HAVING date = MAX(date);
