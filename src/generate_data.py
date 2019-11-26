import random


def _randoms_from_file(filename, count):
    res = []
    try:
        f = open(filename, "r")
        lines = f.read().splitlines()
        f.close()
        for i in range(count):
            res.append(random.choice(lines))
    except OSError:
        print("Can't open " + filename)
    finally:
        return res


def _get_names(count):
    fns = _randoms_from_file("first_names.txt", count)
    lns = _randoms_from_file("last_names.txt", count)
    names = []
    for i in range(count):
        names.append(fns[i] + " " + lns[i])
    return names


def _get_salaries(count):
    salaries = []
    for i in range(count):
        salaries.append(random.randint(2, 40) * 1000)
    return salaries


def _get_ages(count):
    ages = []
    for i in range(count):
        ages.append(random.randint(18 + (i * 2) % 41, 100 - (i // 2) % 41))
    return ages


def _get_specialities(count):
    return _randoms_from_file("specialities.txt", count)


def _get_cabinets(count):
    r = count // 3 + 1
    cabs = [100 + i for i in range(r)] + \
           [200 + i for i in range(r)] + \
           [300 + i for i in range(r)]
    random.shuffle(cabs)
    return cabs[:count]


def _get_date_time(count, start_year, end_year):
    res = []
    for i in range(count):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 31 - int((month % 2 == 0) == (month < 8)) -
                             2 * int(month == 2))
        hour = random.randint(8, 15)
        res.append(["%d-%02d-%02d" % (year, month, day),
                    "%02d:%s:00" % (hour, random.choice(['00', '30']))])
    return res


def _insert_employees(count):
    names = _get_names(count)
    salaries = _get_salaries(count)
    emp = ""
    for i in range(count):
        emp = emp + "INSERT INTO Employee(id, name, salary)" + \
                    " values(%d, '%s', %d);\n" % (i + 1, names[i], salaries[i])
    n_docs = count // 2 + count % 2
    specs = _get_specialities(n_docs)
    cabs = _get_cabinets(n_docs)
    doc = ""
    for i in range(n_docs):
        doc = doc + "INSERT INTO Doctor(employee_id, speciality, cabinet)" + \
                    " values(%d, '%s', %d);\n" % (i + 1, specs[i], cabs[i])
    ass = ""
    for i in range(n_docs, count):
        ass = ass + "INSERT INTO DoctorsAssistant(employee_id, assists)" + \
                    " values(%d, %d);\n" % (i + 1, i % n_docs + 1)
    return emp + doc + ass


def _insert_clients(count):
    names = _get_names(count)
    ages = _get_ages(count)
    cln = ""
    ins = "INSERT INTO Client(id, name, age)"
    for i in range(count):
        cln = cln + ins + " values(%d, '%s', %d);\n"\
            % (i + 1, names[i], ages[i])
    return cln


# May generate less items than count to avoid duplicates
def _insert_apps(count, n_docs, n_clns, start_year, end_year):
    dids = range(1, n_docs + 1)
    cids = range(1, n_clns + 1)
    dates = _get_date_time(count, start_year, end_year)
    ins = "INSERT INTO Appointment(\
doctor_id, client_id, appointment_date, appointment_time)"
    app = set()
    for i in range(count):
        s = ins + " values(%d, %d, '%s', '%s');\n" % \
            (random.choice(dids), random.choice(cids),
             dates[i][0], dates[i][1])
        app.add(s)
    res = ""
    for s in app:
        res = res + s
    return res


def get_insert_statements(seed=None, employee=0, client=0,
                          appointment=0, start_year=2019, end_year=2019):
    if seed != "None" and seed:
        random.seed(int(seed))
    res = _insert_employees(employee) + _insert_clients(client) + \
        _insert_apps(appointment, employee // 2 + employee % 2, client,
                     start_year, end_year)
    return res
