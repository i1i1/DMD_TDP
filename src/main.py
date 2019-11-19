#!/usr/bin/env python3
import db

test = "INSERT INTO Employee(id, name, salary) values(1, 'Ivan', 300)"


def main():
    with db.init_db() as d:
        with d.cursor() as c:
            print("Initing DB...")
            c.execute(open("init.sql", "r").read())
            d.commit()

        with d.cursor() as c:
            print("Generating...")
            c.execute(test)
            d.commit()

        with d.cursor() as c:
            print("Querying...")
            c.execute("SELECT * FROM Employee")
            for row in c.fetchall():
                print(*row)
    return 0


if __name__ == '__main__':
    exit(main())
