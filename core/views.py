from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from . import serializers, models
from .models import BankTransfer


# Create your views here.


def make_transfers(request):
    transactions = models.BankTransfer.objects.filter(is_open=True).all()
    success_ids = []
    faiL_ids = []
    for trans in transactions:
        trans.runtransfer()
        if trans.is_success:
            success_ids.append(trans.id)
        else:
            faiL_ids.append(trans.id)

    return Response(
        {"success_ids": success_ids, "faiL_ids": faiL_ids},
        status=status.HTTP_200_OK,
    )

class BankCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCustomersSerializer
    queryset = models.BankCustomer.objects.order_by('id').all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        # 'name':['exact'],
        'adress': ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
    }


class BankTransferViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankTransferSerializer
    queryset = models.BankTransfer.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_serializer_class(self):
        if self.action == "run_transfer":
            return serializers.RunTransferSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=["post"], url_path="run-transfer")
    def run_transfer(self, request, pk):
        transfer = models.BankTransfer.objects.filter(pk=pk).first()
        transfer.run_transfer()


        if transfer.is_success:
            return Response({"error": "Transaction wurde erfolgreich durchgeführt"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": transfer.executionlog}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankAccount.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
