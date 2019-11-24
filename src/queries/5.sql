create or replace function get_apps_number(
    did integer,
    sd date,
    ed date
)
returns integer as $n_visits$
declare

    n_visits integer;
begin
	select count(id)
	from Employee join Appointment on id = doctor_id
	where appointment_date >= sd and
		  appointment_date < ed and
		  id = did
	group by id
	into n_visits;
	return n_visits;
end;
$n_visits$ LANGUAGE plpgsql;

select distinct name
from Employee join Appointment on id = doctor_id
where get_apps_number(id, date (current_date - interval '10 years'), current_date) >= 100 and
	  get_apps_number(id, date (current_date - interval '10 years'), date (current_date - interval '9 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '9 years'), date (current_date - interval '8 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '8 years'), date (current_date - interval '7 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '7 years'), date (current_date - interval '6 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '6 years'), date (current_date - interval '5 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '5 years'), date (current_date - interval '4 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '4 years'), date (current_date - interval '3 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '3 years'), date (current_date - interval '2 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '2 years'), date (current_date - interval '1 years')) >= 5 and
	  get_apps_number(id, date (current_date - interval '1 years'), current_date) >= 5