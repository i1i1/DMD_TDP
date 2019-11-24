#!/usr/bin/env python3
import os
import db

from flask import Flask, render_template, request
from generate_data import get_insert_statements
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def inno_query(name):
    def get_query(**kargs):
        return open(os.path.join("queries/", name + ".sql")).read() % kargs
    return get_query


app = Flask(__name__)
d = db.init_db()

queries = {
    "1": {
        "__func__": inno_query("1"),
        "__name__": "Query 1",
        "name": str,
    },
    "2": {
        "__func__": inno_query("2"),
        "__name__": "Query 2",
    },
    "3": {
        "__func__": inno_query("3"),
        "__name__": "Query 3",
    },
    "4": {
        "__func__": inno_query("4"),
        "__name__": "Query 4",
    },
    "5": {
        "__func__": inno_query("5"),
        "__name__": "Query 5",
    },
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


def clear_tables():
    with d.cursor() as c:
        c.execute(open("clear.sql", "r").read())
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
            try:
                return c.fetchall()
            except Exception:
                return []


def render_query(query):
    max_lines = 40

    results = get_from_table(query)
    if len(query.splitlines()) > max_lines:
        query = '\n'.join(query.splitlines()[:max_lines]) + "\nToo many lines"
    return render_template("result.html",
                           name="Results",
                           css=highlight_css(),
                           query=highlight_sql(query),
                           results=results)


def render_err(html, err, query):
    return render_template(html,
                           error="Here is some error in your code:",
                           errormsg=str(err),
                           css=highlight_css(),
                           query=highlight_sql(query))


@app.route('/')
def url_home():
    buttons = {
        "Custom query": "/custom_query",
        "Populate": "/populate",
    }
    for q in queries.keys():
        buttons[q] = "/query/" + q

    return render_template("home.html", buttons=buttons, tmp=buttons)


@app.route('/populate', methods=['POST', 'GET'])
def url_populate():
    args = {
        "seed": str,
        "employee": int,
        "client": int,
        "appointment": int,
        "start_year": int,
        "end_year": int,
    }

    if request.method == 'GET':
        return render_template("query.html", error="", url='/populate',
                               name="Populate",
                               args=args.keys())

    query = ""
    clear_tables()

    try:
        d = dict(request.form)
        for k, v in d.items():
            d[k] = args[k](v)
        return render_query(get_insert_statements(**d))
    except Exception as e:
        return render_err("query.html", e, query)


@app.route('/query/<name>', methods=['POST', 'GET'])
def url_query(name):
    if request.method == 'GET':
        return render_template("query.html", error="", url='/query/'+name,
                               name=queries[name]["__name__"],
                               args=queries[name].keys())

    query = ""

    try:
        d = dict(request.form)
        for k, v in d.items():
            d[k] = queries[name][k](v)

        query = queries[name]["__func__"](**d)
        return render_query(query)
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
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
