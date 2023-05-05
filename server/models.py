from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    signups = db.relationship("Signup", backref="activity")
    campers = db.relationship("Camper", backref="activity")

    serialize_rules = ("-created_at", "-updated_at", "-signups", "-campers")


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ("-created_at", "-updated_at")


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", backref="camper")
    acitivities = db.relationship("Activity", backref="camper")

    serialize_rules = ("-created_at", "-updated_at",
                       "-signups", "-acitivities")

    @validates("name")
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Camper must have a name")
        return name

    @validates("age")
    def validates_age(self, key, age):
        if 8 <= age <= 18:
            return age
        raise ValueError("Age must be between 8 and 18 years")


# add any models you may need.
