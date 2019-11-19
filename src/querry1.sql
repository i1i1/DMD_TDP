SELECT DISTINCT Employee.name
FROM Appointment JOIN Client ON Appointment.client_id = Client.id
JOIN Doctor ON Doctor.employee_id = Appointment.doctor_id
JOIN Employee ON Doctor.employee_id = Employee.id
WHERE Client.name = %name AND (Doctor.name LIKE "%M%" OR Doctor.name LIKE "%L%") AND
(NOT Doctor.name LIKE "M% M%") AND (NOT Doctor.name LIKE "L% L%")
HAVING datetime = MAX(datetime)
