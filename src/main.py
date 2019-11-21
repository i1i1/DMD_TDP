#!/usr/bin/env python3
import db

from generate_data import get_insert_statements


def main():
    with db.init_db() as d:
        with d.cursor() as c:
            print("Initing DB...")
            c.execute(open("init.sql", "r").read())
            d.commit()

        for line in get_insert_statements(seed=1,
                                          Employee=10,
                                          Client=50,
                                          Appointment=100).splitlines():
            with d.cursor() as c:
                print(line)
                c.execute(line)
                d.commit()

        with d.cursor() as c:
            print("Querying...")
            c.execute("SELECT * FROM Appointment")
            for row in c.fetchall():
                print(*row)
    return 0


if __name__ == '__main__':
    exit(main())
