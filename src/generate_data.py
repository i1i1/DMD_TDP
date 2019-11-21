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
        salaries.append(random.randint(2, 500) * 1000)
    return salaries


def _get_ssns(count):
    ssns = []
    for i in range(count):
        candidate = random.randint(10**8, 10**9 - 1)
        while candidate in ssns:
            candidate = random.randint(10**8, 10**9 - 1)
        ssns.append(candidate)
    return ssns


def _get_specialities(count):
    return _randoms_from_file("specialities.txt", count)


def _get_cabinets(count):
    r = count // 3 + 1
    cabs = [100 + i for i in range(r)] + \
           [200 + i for i in range(r)] + \
           [300 + i for i in range(r)]
    random.shuffle(cabs)
    return cabs[:count]


def _get_date_time(count):
    res = []
    for i in range(count):
        year = random.randint(2018, 2019)
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
    ssns = _get_ssns(count)
    cln = ""
    ins = "INSERT INTO Client(id, name, ssn)"
    for i in range(count):
        cln = cln + ins + " values(%d, '%s', %d);\n"\
            % (i + 1, names[i], ssns[i])
    return cln


def _insert_apps(count, n_docs, n_clns):
    dids = range(1, n_docs + 1)
    cids = range(1, n_clns + 1)
    dates = _get_date_time(count)
    ins = "INSERT INTO Appointment(doctor_id, client_id, date, time, approved)"
    app = ""
    for i in range(count):
        app = app + ins + " values(%d, %d, '%s', '%s', TRUE);\n" % \
            (random.choice(dids), random.choice(cids),
             dates[i][0], dates[i][1])
    return app


def get_insert_statements(seed=None, Employee=0, Client=0,
                          Appointment=0):
    if seed is not None:
        random.seed(seed)
    res = _insert_employees(Employee) + _insert_clients(Client) + \
        _insert_apps(Appointment, Employee // 2 + Employee % 2, Client)
    return res
