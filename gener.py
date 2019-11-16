#!/usr/bin/env python3
import db

test = '''\
CREATE SCHEMA hospital;

CREATE TABLE Employee(
    id serial PRIMARY KEY,
    name varchar(30),
    salary money
);

CREATE TABLE Client(
    id serial PRIMARY KEY,
    name varchar(30),
    ssn integer UNIQUE,
    credit_info varchar(10)
);

CREATE TABLE Doctor(
    employee_id integer references Employee,
    speciality varchar(30),
    cabinet integer,
    PRIMARY KEY (employee_id)
);

CREATE TABLE DoctorsAssistant(
    empployee_id integer references Employee,
    assists integer references Doctor,
    PRIMARY KEY (empployee_id)
);

CREATE TABLE Appointment(
    doctor_id integer references Doctor,
    client_id integer references Client,
    datetime timestamptz,
    approved boolean,
    PRIMARY KEY (doctor_id, client_id, datetime)
);

CREATE TABLE Inventory(
    id serial PRIMARY KEY,
    usage_receipt varchar(30)
);

CREATE TABLE InventoryRequests(
    inventory_id integer references Inventory,
    assistant_id integer references DoctorsAssistant,
    date timestamptz,
    approved boolean,
    PRIMARY KEY(inventory_id, date)
);
CREATE TABLE Procedures(
    id serial PRIMARY KEY,
    assistant_id integer references DoctorsAssistant,
    client_id integer references Client,
    inventory_id integer references Inventory,
    result text,
    cost money,
    date timestamptz
);
CREATE TABLE PatientRecord(
    id serial PRIMARY KEY,
    personal_info text,
    client_id integer references Client
);

CREATE TABLE TreatmentReport(
    id serial PRIMARY KEY,
    doctor_id integer references Doctor,
    record_id integer references PatientRecord,
    date timestamptz,
    description text
);

CREATE TABLE TreatmentTests(
    report_id integer references TreatmentReport,
    procedure_id integer references Procedures,
    PRIMARY KEY (report_id, procedure_id)
);

CREATE TABLE Drug(
    name varchar(30) PRIMARY KEY,
    requires_prescription boolean,
    amount integer
);

CREATE TABLE Prescribed(
    record_id integer references PatientRecord,
    drug varchar(30) references Drug,
    prescribed_amount integer,
    PRIMARY KEY(record_id, drug)
);

CREATE TABLE OnlineHelp(
    employee_id integer references Employee,
    client_id integer references Client,
    date timestamptz,
    question text,
    answer text,
    PRIMARY KEY (client_id, date)
);

CREATE TABLE DrugSold(
    drug varchar(30) references Drug,
    client_id integer references Client,
    amount integer,
    datetime timestamptz,
    PRIMARY KEY (client_id, datetime)
);
'''


def main():
    with db.init_db() as d:
        with d.cursor() as c:
            print("Generating...")
            c.execute(test)
            d.commit()
    return 0


if __name__ == '__main__':
    exit(main())
