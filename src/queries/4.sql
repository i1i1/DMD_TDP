WITH visits_on_last_month AS

(select name, count(name) as visits, age 
from Client as c inner join Appointment as a on c.id = a.client_id 
where date_part('year', a.appointment_date) = date_part('year', current_date) and date_part('month', age(a.appointment_date)) = 0 and current_date > a.appointment_date
group by c.name, c.age)

select sum
(
case
when visits < 3 and age < 50 then 200
when visits < 3 and age >= 50 then 400
when visits >= 3 and age < 50 then 250
when visits >=3 and age >= 50 then 500
end
) as Income
from visits_on_last_month; 


