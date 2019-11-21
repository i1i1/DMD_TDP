#!/usr/bin/env python3
import db

from flask import Flask, render_template, request
from generate_data import get_insert_statements
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


app = Flask(__name__)
d = db.init_db()


def highlight_css():
    return HtmlFormatter().get_style_defs('.highlight')


def highlight_sql(src):
    lex = get_lexer_by_name('sql')
    fmt = HtmlFormatter(linenos=True, cssclass="highlight")
    return highlight(src, lex, fmt)


def init_tables():
    print("Initing DB...")
    with d.cursor() as c:
        c.execute(open("init.sql", "r").read())
        d.commit()


def get_from_table(query):
    print("Quering...")
    with d.cursor() as c:
        c.execute('SAVEPOINT sp1')
        try:
            c.execute(query)
        except Exception as e:
            c.execute('ROLLBACK TO SAVEPOINT sp1')
            raise e
        else:
            d.commit()
            return c.fetchall()


def gener_items():
    lines = get_insert_statements(seed=1, Employee=10,
                                  Client=50, Appointment=100).splitlines()
    for line in lines:
        with d.cursor() as c:
            c.execute(line)
            d.commit()


@app.route('/')
def url_home():
    buttons = {"Query 1": "/query/1",
               "Query 2": "/query/2",
               "Query 3": "/query/3",
               "Query 4": "/query/4",
               "Query 5": "/query/5",
               "Custom query": "/custom_query"}
    return render_template("home.html", buttons=buttons)


@app.route('/query/<int:num>')
def url_query(num):
    query = highlight_sql(open("query" + str(num) + ".sql", "r").read())
    return render_template("result.html",
                           name="Query " + str(num),
                           css=highlight_css(),
                           query=query,
                           results=get_from_table(query))


@app.route('/custom_query', methods=['POST', 'GET'])
def url_custom_query():
    if request.method == 'GET':
        return render_template("query.html", error="")

    query = request.form["query"]

    try:
        results = get_from_table(query)
        return render_template("result.html",
                               name="Results",
                               css=highlight_css(),
                               query=highlight_sql(query),
                               results=results)
    except Exception as e:
        print(e)
        return render_template("query.html",
                               error="Here is some in error in your query:",
                               errormsg=str(e),
                               css=highlight_css(),
                               query=highlight_sql(query))


if __name__ == '__main__':
    init_tables()
    gener_items()
    app.run(host="0.0.0.0")
