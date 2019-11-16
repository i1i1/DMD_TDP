import os


def _init_db():
    print(os.getenv("DB_TYPE"))
    if os.getenv("DB_TYPE") == 'mysql':
        import pymysql
        return pymysql.Connect(host=os.getenv("DB_HOST"),
                               user=os.getenv("DB_USER"),
                               passwd=os.getenv("DB_PASSWORD"),
                               db=os.getenv("DB_NAME"))
    elif os.getenv("DB_TYPE") == 'postgres':
        import psycopg2
        s = "dbname='%s' user='%s' host='%s' password='%s'" % \
            (os.getenv("DB_NAME"), os.getenv("DB_USER"),
             os.getenv("DB_HOST"), os.getenv("DB_PASSWORD"))
        return psycopg2.connect(s)
    else:
        raise Exception("Unknown DB_TYPE")


def init_db():
    from time import sleep
    while True:
        try:
            return _init_db()
        except Exception:
            print("Sleeping...")
            sleep(1)
