from functools import reduce
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import Patient, db
from sqlalchemy import desc, asc
from faker import Faker
from datetime import date
from random import *
from .ApiCommunication import Messages, Patienten
from .ApiCommunication.Models2 import Content, MessagePost
from .FrontendModels.Patient import Patient

"""
hier staan alle routes van de api
"""

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/usecase1")
def usecase1():
    return render_template("usecase1.html")


# vraagt alle patienten op, bouwt de template op en geeft ze terug
@views.route("/usecase2", methods=["GET"])
def usecase2():
    # all_patients = Patient.query.order_by(desc(Patient.id)).all()
    # vraagt alle patienten op
    all_patients = list(
        map(
            lambda patient: Patient.fromBewellApiModel(patient),
            Patienten.getPatienten(""),
        )
    )
    # bouwt de template ne geeft ze terug
    return render_template("usecase2.html", patients=all_patients)


@views.route("/addDummyData", methods=["POST"])
def addDummyData():
    if request.method == "POST":
        fakerProvider = Faker()
        rnd = Random()
        for i in range(30):
            new_patient = Patient(
                afdeling=rnd.randint(1, 5),
                kamer=rnd.randint(1, 5),
                familienaam=fakerProvider.last_name(),
                voornaam=fakerProvider.first_name(),
                geboortedatum=fakerProvider.date_of_birth().__str__(),
                dieet="Normaal",
                laatste_bevraging=date.today().__str__(),
            )
            db.session.add(new_patient)
            db.session.commit()
    return redirect(url_for("views.usecase2"))


@views.route("/deleteData", methods=["POST"])
def deleteData():
    if request.method == "POST":
        Patient.query.delete()
        db.session.commit()
    return redirect(url_for("views.usecase2"))


@views.route("/deleteRecord/<patientId>", methods=["POST"])
def deleteRecord(patientId):
    if request.method == "POST":
        patient = Patient.query.get(patientId)
        if patient:
            db.session.delete(patient)
            db.session.commit()
    return redirect(url_for("views.usecase2"))


# vraagt alle patienten op gefilterd op basis van het 'searchquery veld van de meegestuurde form en bouwt dan de usecase2.html template op met de gevonden patienten'
@views.route("/filterData/", methods=["post"])
def filterData():
    import re

    # neemt de searchquery uit de meegestuurde form en converteerd hem naar het juiste formaat
    searchQuery = request.form.get("searchQuery").__str__().strip()
    search = "{}".format(searchQuery.lower().strip())
    print("searching for: ", search)
    # filtered_patients = Patient.query.filter(Patient.voornaam.like(search)|
    #                                          Patient.familienaam.like(search)
    #                                          ).all()
    # filterd de patienten op basis van de searchquery: als de searchquery voornaam of familienaam of een combinatie van beide bevat zal deze patient in filtered patients worden gestoken
    filtered_patients = list(
        filter(
            lambda patient: search
            in patient.first_name.lower() + " " + patient.last_name.lower(),
            map(
                lambda patient: Patient.fromBewellApiModel(patient),
                Patienten.getPatienten(""),
            ),
        )
    )
    print("de gefilterde patienten: ", filtered_patients)
    return render_template(
        "usecase2.html", patients=filtered_patients, searchValue=searchQuery
    )


# geeft de template terug om een nieuwe patient aan te maken
@views.route("/addPatientRequest/", methods=["GET"])
def addPatientRequest():
    return render_template("addNewPatient.html", views=views)


# deze post route gebruikt de data in de meegestuurde form om een nieuwe patient aan te maken
@views.route("/newPatient", methods=["POST"])
def newPatient():
    try:
        patientToAdd = Patient(
            afdeling=int(request.form["afdeling"]),
            kamer=int(request.form["kamer"]),
            familienaam=request.form["familienaam"],
            voornaam=request.form["voornaam"],
            geboortedatum=request.form["geboortedatum"],
            dieet=request.form["dieet"],
            laatste_bevraging=request.form.get("laatste_bevraging"),
        )
        db.session.add(patientToAdd)
        db.session.commit()
        flash("patient is toegevoegd")
        return redirect(url_for("views.usecase2"))
    except ValueError:
        flash("geef een correcte waarde in")
        return redirect(url_for("views.addPatientRequest"))


# geeft de template terug om een nieuw berichtje aan te maken
@views.route("/getNewMessage", methods=["get"])
def getNewMessage():
    PatientNamen = list(
        map(
            lambda patient: {
                "id": patient.id,
                "name": f"{patient.first_name}_{patient.last_name}",
            },
            Patienten.getPatienten(""),
        )
    )
    mostRecentMessageRaw = Messages.getMostRecentMessage()
    lastMessage = {
        "inhoud": mostRecentMessageRaw.text,
        "ontvanger": next(
            filter(
                lambda patientNaam: patientNaam.get("id")
                == mostRecentMessageRaw.recipient_id,
                PatientNamen,
            )
        ).get("name"),
    }
    return render_template(
        "addNewMessage.html",
        patienten=PatientNamen,
        lastMessage=lastMessage,
        views=views,
    )


# deze post route gebruikt de data in de meegestuurde form om een nieuw berichtje aan te maken via de backend
@views.route("/postNewMessage", methods=["POST"])
def postNewMessage():
    # bouwt de message op op basis van de data in de meegestuurde form
    newMessage = MessagePost(
        recipient_id=int(request.form["recipientId"]),
        content=Content(text=str(request.form["message"])),
    )
    # stuurt de opgebouwde message door naar de backend laag en geeft een passend bericht op basis van de feedback(true bij succes of false bij mislukking)
    if Messages.PostNewMessage(newMessage):
        return render_template(
            "genericMessage.html",
            message="berichtje is succesvol aangemaakt",
            views=views,
        )
    else:
        return render_template(
            "genericMessage.html",
            message="er is een fout opgetreden bij het doorsturen naar de bewell api",
            views=views,
        )
