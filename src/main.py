#!/usr/bin/env python3
import os
import db

from flask import Flask, render_template, request
from generate_data import get_insert_statements
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


app = Flask(__name__)
d = db.init_db()

queries = {
    "1": { "name": str },
    "2": {},
    "3": {},
    "4": {},
    "5": {},
}


def highlight_css():
    return HtmlFormatter().get_style_defs('.highlight')


def highlight_sql(src):
    lex = get_lexer_by_name('sql')
    fmt = HtmlFormatter(cssclass="highlight")
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
    lines = get_insert_statements(seed=0, Employee=100,
                                  Client=500, Appointment=1000).splitlines()
    for line in lines:
        with d.cursor() as c:
            c.execute(line)
            d.commit()


def render_query(query):
    return render_template("result.html",
                           name="Results",
                           css=highlight_css(),
                           query=highlight_sql(query),
                           results=get_from_table(query))


def render_err(html, err, query):
     return render_template(html,
                            error="Here is some in error in your query:",
                            errormsg=str(err),
                            css=highlight_css(),
                            query=highlight_sql(query))


@app.route('/')
def url_home():
    buttons = {"Custom query": "/custom_query"}
    for q in queries.keys():
        buttons["Query " + q] = "/query/" + q
    return render_template("home.html", buttons=buttons, tmp=buttons)


@app.route('/query/<name>', methods=['POST', 'GET'])
def url_query(name):
    if request.method == 'GET':
        return render_template("query.html", error="", name=name,
                               args=queries[name].keys())

    try:
        d = dict(request.form)
        for k, v in d.items():
            d[k] = queries[name][k](d[k])

        query = open(os.path.join("queries/", name + ".sql"), "r").read()
        return render_query(query % d)
    except Exception as e:
        return render_err("query.html", e, query)


@app.route('/custom_query', methods=['POST', 'GET'])
def url_custom_query():
    if request.method == 'GET':
        return render_template("custom_query.html", error="")

    query = request.form["query"]

    try:
        return render_query(query)
    except Exception as e:
        return render_err("custom_query.html", e, query)


if __name__ == '__main__':
    init_tables()
    gener_items()
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
