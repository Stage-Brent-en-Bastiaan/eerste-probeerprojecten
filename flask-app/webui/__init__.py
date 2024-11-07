import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "database.db"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    afdeling = db.Column(db.Integer)
    kamer = db.Column(db.Integer)
    familienaam = db.Column(db.String(50))
    voornaam = db.Column(db.String(50))
    geboortedatum = db.Column(db.String(10))
    dieet = db.Column(db.String(50))
    laatste_bevraging = db.Column(db.String(10))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # generate secret key and set it in the app
    app.secret_key = os.urandom(24)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
