#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import db, Activity, Signup, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/campers', methods=["GET", "POST"])
def get_campers():
    if request.method == 'GET':
        campers = Camper.query.all()
        return [camper.to_dict() for camper in campers]
    elif request.method == 'POST':
        data = request.get_json()

        try:
            camper = Camper(
                name=data.get("name"),
                # name=data['name'],
                age=data['age'],
            )
            db.session.add(camper)
            db.session.commit()

            return camper.to_dict()
        except ValueError:
            return {
                "error": "Validation Error",
            }


@app.route('/campers/<int:id>')
def get_camper_by_id(id):
    camper = Camper.query.filter_by(id=id).first()

    if camper:
        return camper.to_dict(rules=("signups", ))

    return {
        "message": "The camper was not found",
    }


@app.route('/campers/<int:id>', methods=["DELETE", "POST"])
def delete_camper(id):
    if request.method == 'DELETE':
        camper = Camper.query.filter_by(id=id).first()
        db.session.delete(camper)
        db.session.commit()
    return {
        "message": "Deleted Successfully",
    }


if __name__ == '__main__':
    app.run(port=5555, debug=True)
