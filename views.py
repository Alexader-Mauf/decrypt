from django.db import transaction
from django.shortcuts import render

from . import models

def testest(request):
    return render(request, "bootstraptest.html")

def decode(request):
    return render(request, "decode.html")

def index(request):
    return render(request, "home.html")


def load_secretnote(request, uuid):
    try:
        secretnote = models.SecretMsg.objects.get(uuid=uuid)
    except:
        return render(request, "create_failed.html")

    return render(request, "showsecretnote.html", {
        "secretnote": secretnote
    })


def create_secretnote(request):
    # write action
    # wir erzeugen einen Datenbankeintrag mit dem selbstgebauten model
    # sowie Djangos Framework
    secret_message = models.SecretMsg.objects.create(
        message=request.POST.get("message")
    )
    # wir setzten/speichern den Datenbakeintrag
    # ohne diesen Befehl ist der vorangegangene Befehl nutzlos(ohne Effekt auf die Datenbank)
    secret_message.save()
    return render(request, "create_success.html", {
        "secret_message": secret_message
    })

