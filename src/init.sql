CREATE SCHEMA hospital;

CREATE TABLE Employee(
    id integer PRIMARY KEY,
    name varchar(30),
    salary money
);

CREATE TABLE Client(
    id integer PRIMARY KEY,
    name varchar(30),
    ssn integer UNIQUE,
    credit_info varchar(10)
);

CREATE TABLE Doctor(
    employee_id integer references Employee(id),
    speciality varchar(30),
    cabinet integer,
    PRIMARY KEY (employee_id)
);

CREATE TABLE DoctorsAssistant(
    employee_id integer references Employee(id),
    assists integer references Doctor(employee_id),
    PRIMARY KEY (employee_id)
);

CREATE TABLE Appointment(
    doctor_id integer references Doctor(employee_id),
    client_id integer references Client(id),
    date date,
    time time,
    approved boolean,
    PRIMARY KEY (doctor_id, client_id, date, time)
);

CREATE TABLE Inventory(
    id integer PRIMARY KEY,
    usage_receipt varchar(30)
);

CREATE TABLE InventoryRequests(
    inventory_id integer references Inventory(id),
    assistant_id integer references DoctorsAssistant(employee_id),
    date date,
    time time,
    approved boolean,
    PRIMARY KEY(inventory_id, date, time)
);
CREATE TABLE Procedures(
    id integer PRIMARY KEY,
    assistant_id integer references DoctorsAssistant(employee_id),
    client_id integer references Client(id),
    inventory_id integer references Inventory(id),
    result text,
    cost money,
    date date,
    time time
);
CREATE TABLE PatientRecord(
    id integer PRIMARY KEY,
    personal_info text,
    client_id integer references Client(id)
);

CREATE TABLE TreatmentReport(
    id integer PRIMARY KEY,
    doctor_id integer references Doctor(employee_id),
    record_id integer references PatientRecord(id),
    date date,
    time time,
    description text
);

CREATE TABLE TreatmentTests(
    report_id integer references TreatmentReport(id),
    procedure_id integer references Procedures(id),
    PRIMARY KEY (report_id, procedure_id)
);

CREATE TABLE Drug(
    name varchar(30) PRIMARY KEY,
    requires_prescription boolean,
    amount integer
);

CREATE TABLE Prescribed(
    record_id integer references PatientRecord(id),
    drug varchar(30) references Drug(name),
    prescribed_amount integer,
    PRIMARY KEY(record_id, drug)
);

CREATE TABLE OnlineHelp(
    employee_id integer references Employee(id),
    client_id integer references Client(id),
    date date,
    time time,
    question text,
    answer text,
    PRIMARY KEY (client_id, date)
);

CREATE TABLE DrugSold(
    drug varchar(30) references Drug(name),
    client_id integer references Client(id),
    amount integer,
    date date,
    time time,
    PRIMARY KEY (client_id, date, time)
);

