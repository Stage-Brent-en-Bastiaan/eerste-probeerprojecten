from django import template
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *
from django.shortcuts import render
from ApiCommunication import Patienten, Messages, Models2


def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render(request=request))


# renderd de patientenlijst met alle patienten
def getPatients(request):
    # vraagt alle patienten op
    all_patients = list(
        map(
            lambda patient: Patient.fromBewellApiModel(patient),
            Patienten.getPatienten(""),
        )
    )
    # bouwt de template en geeft ze terug
    template = loader.get_template("patients.html")
    context = {
        "patients": all_patients,
    }
    return HttpResponse(template.render(context, request))


# renderd de newmessage form
def getSendMessage(request):
    # neem id van de gekozen patient uit de form
    recipient_id = request.POST.get("patientId")
    recipient_name = request.POST.get("patientName")

    # en steek hem in een cookie
    request.session["recipient_id"] = recipient_id
    # get meest recente bericht
    mostRecentMessageRaw = Messages.getMostRecentMessage()
    lastMessage = {
        "inhoud": mostRecentMessageRaw.text,
        "ontvanger": Patienten.getPatient(
            mostRecentMessageRaw.recipient_id
        ).full_name(),
        "verzender": Patienten.getPatient(mostRecentMessageRaw.author_id).full_name(),
    }
    # bouw de template en geef ze terug
    form = NewMessageForm()
    template = loader.get_template("addNewMessage.html")
    context = {
        "lastMessage": lastMessage,
        "recipient_id": recipient_id,
        "recipient_name": recipient_name,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


# filterd de patienten op basis van de searchquery en renderd dan de patienten tabel met deze gefilterde patientenlijst
def filterData(request):
    import re

    # neemt de searchquery uit de meegestuurde form en converteerd hem naar het juiste formaat
    searchQuery = request.POST.get("searchQuery").__str__().strip()
    search = "{}".format(searchQuery.lower().strip())
    print("searching for: ", search)
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
    # bouw de template en geef ze terug
    template = loader.get_template("patients.html")
    context = {"patients": filtered_patients, "searchValue": searchQuery}
    return HttpResponse(template.render(context, request))


# post een nieuw bericht richting de bewell api
def postNewMessage(request):
    # bouwt de message op op basis van de data in de meegestuurde form en de recipient id cookie
    newMessage = Models2.MessagePost(
        recipient_id=request.session.get("recipient_id"),
        content=Models2.Content(text=str(request.POST.get("message"))),
    )
    # stuurt de opgebouwde message door naar de backend laag en geeft een passend bericht op basis van de feedback
    if Messages.PostNewMessage(newMessage):
        return render(
            request,
            "genericMessage.html",
            {"message": "bericht is succesvol aangemaakt"},
        )
    else:
        return render(
            request,
            "genericMessage.html",
            {"er is een fout opgetreden bij het versturen van het bericht"},
        )
