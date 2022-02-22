from flask import json

from abcTEST import db


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
