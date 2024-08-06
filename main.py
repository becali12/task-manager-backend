from flask import Flask
from db_utils import init_db, select_table, insert_user

app = Flask(__name__)

@app.route('/')
def home():
    return '{"Hello": "World"}'

@app.route('/init')
def initialise():
    return '{"success": "True"}' if init_db() else '{"success": "False"}'


@app.route('/addUser')
def add_user():
    test_user = {"name": "Cristi", "last_connected": "2024-08-06 12:34:56"}
    return '{"success": "True"}' if insert_user(test_user) else '{"success": "False"}'


@app.route('/table/<string:table_name>')
def view_table(table_name):
    results = select_table(table_name)
    return f'<p>{results}</p>'