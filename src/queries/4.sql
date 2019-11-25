WITH visits_on_last_month AS

(select name, count(name) as visits, age
from Client as c inner join Appointment as a on c.id = a.client_id
where DATE_PART('month',appointment_date) = DATE_PART('month',CURRENT_DATE - interval '1 month')
group by c.name, c.age)

select sum
(
case
when visits < 3 and age < 50 then visits*200
when visits < 3 and age >= 50 then visits*400
when visits >= 3 and age < 50 then visits*250
when visits >=3 and age >= 50 then visits*500
end
) as Income
from visits_on_last_month;