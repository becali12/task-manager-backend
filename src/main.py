from flask import Flask, request, jsonify, make_response
from db_utils import init_db, select_table, insert_user

app = Flask(__name__)


def build_response(statusCode : int, message : str) -> dict: 
    response = make_response(jsonify({"message": message}, statusCode))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response


@app.route('/', methods = ['GET'])
def home():
    return '{"Hello": "World"}'


@app.route('/init', methods = ['GET'])
def initialise():
    return build_response(200, "OK") if init_db() else build_response(500, "Internal Server Error")


@app.route('/addUser', methods = ['OPTIONS', 'POST'])
def add_user():
    if request.method == 'OPTIONS':
        return build_response(200, 'OK')
    elif request.method == 'POST':
        data = request.get_json()
        user = data.get('user', None)

        if not user:
            return build_response(400, "Bad request: no user provided, or was wrongly formatted.")
        
        return build_response(200, "OK") if insert_user(user) else build_response(500, "Internal Server Error")


@app.route('/table/<string:table_name>', methods = ['GET', 'POST'])
def view_table(table_name):
    results = select_table(table_name)
    return f'<p>{results}</p>'