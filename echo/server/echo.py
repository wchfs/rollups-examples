import json
import logging
from os import environ

import flask
import requests
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

dispatcher_url = environ["HTTP_DISPATCHER_URL"]


@app.route("/advance", methods=["POST"])
def advance():
    s_json = hex2json(request.get_json()["payload"])  # make json object from 0x123456... received from request body

    path = s_json["path"]  # recognize HTTP endpoint
    method = s_json["method"]  # recognize HTTP method
    payload = s_json["payload"]  # recognize HTTP payload

    result = {}

    if method == 'GET' and path == '/users':
        result = get_users(payload)

    if method == 'POST' and path == '/users':
        result = add_users(payload)

    if method == 'GET' and path == '/tasks':
        result = get_tasks(payload)

    if method == 'POST' and path == '/tasks':
        result = add_tasks(payload)

    if result != {}:
        response = requests.post(dispatcher_url + "/notice", json={"payload": json2hex(result)})
        app.logger.info(f"Received notice status {response.status_code} body {response.content}")
    else:
        app.logger.info(f"Empty result, so skip notice")

    requests.post(dispatcher_url + "/finish", json={"status": "accept"})

    return "Advance OK", 202


def hex2json(hex_json):
    partial = hex_json[2:]  # partial as 123456...
    content = (bytes.fromhex(partial).decode("utf-8"))  # decode partial from hex to string
    return json.loads(content)  # convert decoded partial to json format


def json2hex(json2encode):
    return "0x" + str(flask.json.dumps(json2encode).encode("utf-8").hex())


def get_users(payload):
    return rows2dict(User.query.all())


def add_users(users_payload):
    user = User(name=users_payload['name'], email=users_payload['email'])
    db.session.add(user)
    db.session.commit()
    return get_users(users_payload)


def get_tasks(payload):
    return rows2dict(Task.query.all())


def add_tasks(tasks_payload):
    task = Task(title=tasks_payload['title'], description=tasks_payload['description'])
    db.session.add(task)
    db.session.commit()
    return get_tasks(tasks_payload)


def rows2dict(rows):
    d = []

    for row in rows:
        rd = {}
        for column in row.__table__.columns:
            rd[column.name] = str(getattr(row, column.name))
        d.append(rd)

    return d


class Task(db.Model):
    id: int
    title: str
    description: str

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class User(db.Model):
    id: int
    name: str
    email: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    email = db.Column(db.String(length=40), nullable=False, unique=True)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


if __name__ == '__main__':
    app.run(debug=True)
