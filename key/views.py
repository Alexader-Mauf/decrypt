from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from . import models
from . import serializers

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

def encode_decode(request):
    status_decode = request.POST.get("decode")
    status_encode = request.POST.get("encode")
    input = request.POST.get("message")

    if status_encode:
    # encode action
        secret_message = models.SecretMsg.objects.create(
        message=input
        )
        secret_message.save()
        return render(request, "create_success.html", {
            "secret_message": secret_message
             })
    elif status_decode:
    # decode action
        try:
            secretnote = models.SecretMsg.objects.get(uuid=input)
        except:
            return render(request, "create_failed.html")

        return render(request, "showsecretnote.html", {
            "secretnote": secretnote
            })

    else:
    # no button pressed
        return
    return render(request, "home.html")

class SecretMsgViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecretMsgSerializer
    queryset = models.SecretMsg.objects.order_by('-uuid')
    permission_classes = []
    authentication_classes = []
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'uuid':['exact'],
        'created_at':['gte', 'lte'],
        'updated_at':['gte', 'lte'],
        'message':[],
    }