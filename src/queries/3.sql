WITH visits_on_last_month_1st_week AS

    (select id, name, count(id) as visits1
    from Client as c inner join Appointment as a on c.id = a.client_id
    where (date_part('year', a.appointment_date) = date_part('year', current_date) and date_part('month', current_date) = date_part('month', a.appointment_date) + 1
    or date_part('month', current_date) = 1 and date_part('year', current_date) - date_part('year', a.appointment_date) = 1)
    and date_part('day', a.appointment_date) >= 1 and date_part('day', a.appointment_date) <= 7
    group by c.id),

visits_on_last_month_2st_week as

    (select id, name, count(id) as visits2
    from Client as c inner join Appointment as a on c.id = a.client_id
    where (date_part('year', a.appointment_date) = date_part('year', current_date) and date_part('month', current_date) = date_part('month', a.appointment_date) + 1
    or date_part('month', current_date) = 1 and date_part('year', current_date) - date_part('year', a.appointment_date) = 1)
    and date_part('day', a.appointment_date) >= 8 and date_part('day', a.appointment_date) <= 14
    group by c.id),

visits_on_last_month_3st_week as
    (select id, name, count(id) as visits3
    from Client as c inner join Appointment as a on c.id = a.client_id
    where (date_part('year', a.appointment_date) = date_part('year', current_date) and date_part('month', current_date) = date_part('month', a.appointment_date) + 1
    or date_part('month', current_date) = 1 and date_part('year', current_date) - date_part('year', a.appointment_date) = 1)
    and date_part('day', a.appointment_date) >= 15 and date_part('day', a.appointment_date) <= 21
    group by c.id),

visits_on_last_month_4th_week as
    (select id, name, count(id) as visits4
    from Client as c inner join Appointment as a on c.id = a.client_id
    where (date_part('year', a.appointment_date) = date_part('year', current_date) and date_part('month', current_date) = date_part('month', a.appointment_date) + 1
    or date_part('month', current_date) = 1 and date_part('year', current_date) - date_part('year', a.appointment_date) = 1)
    and date_part('day', a.appointment_date) >= 22 and date_part('day', a.appointment_date) <= 28
    group by c.id)

select one.id, one.name
from
(visits_on_last_month_1st_week as one inner join visits_on_last_month_2st_week as two on one.name = two.name)
inner join visits_on_last_month_3st_week as three on one.id = three.id
inner join visits_on_last_month_4th_week as four on one.id = four.id
where visits1 >= 2 and visits2 >= 2 and visits3 >= 2 and visits4 >= 2;
