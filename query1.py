#!/usr/bin/python3

import db


def main():
    text = "SELECT * FROM Employee"

    with db.init_db() as d:
        with d.cursor() as c:
            print("Querying...")
            c.execute(text)
            for row in c.fetchall():
                print(*row)

    return 0


if __name__ == '__main__':
    exit(main())
