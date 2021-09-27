from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import Worker, TradePoint, Visit
from . serializers import TradePointSerializer, WorkerSerializer, VisitSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, BaseAuthentication
from phonenumbers import parse


# проверяет, есть ли worker с указанным в URL phone_number
def check_user(self):
    try:
        phone_number = self.request.query_params.get('phone_number', None)
        worker = Worker.objects.filter(phone_number=parse(phone_number, region='RU'))
        if worker:
            return True
        return False
    except AttributeError as ae:
        return False

class VisitView(APIView):
    serializer_class = VisitSerializer

    def post(self, request):
        if not check_user(self):
            return Response('Worker not found or phone_number is not stated')
        date = request.data.get('date')
        place = request.data.get('place')
        coords = request.data.get('coords')
        data = {"date": date, "place": place, "coords": coords}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            visit_saved = serializer.save()
        return Response({"success": "visit '{}' created successfully".format(visit_saved)})


class  GetTradePointsByPhone(APIView):
        lookup_field = 'phone_number'
        serializer_class = TradePointSerializer

        def get(self, request):
            if not check_user(self):
                return Response('Worker not found or phone_number is not stated')
            tradepoints = self.get_queryset()
            serializer = self.serializer_class(tradepoints, many=True)
            return Response(serializer.data)
        
        def get_queryset(self):
            phone_number = self.request.query_params.get('phone_number', None)
            return TradePoint.objects.filter(worker__phone_number=phone_number)