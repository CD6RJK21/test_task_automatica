from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import Worker, TradePoint, Visit
from . serializers import TradePointSerializer, WorkerSerializer, VisitSerializer
from django_filters.rest_framework import DjangoFilterBackend
import  django_filters

class WorkerView(APIView):
    lookup_field = 'worker'
    serializer_class = WorkerSerializer

    def get(self, request):
        workers = Worker.objects.all()
        serializer = self.serializer_class(workers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        data = {"name": name, "phone_number": phone_number}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            workers_saved = serializer.save()
        return Response({"success": "Worker '{}' created successfully".format(workers_saved)})   


class TradePointView(APIView):
    queryset = TradePoint.objects.all()
    serializer_class = TradePointSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = django_filters.CharFilter(field_name='worker__phone_number', lookup_expr='iexact')

    def get(self, request):
        tradepoints = TradePoint.objects.all()
        serializer = TradePointSerializer(tradepoints, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        name = request.data.get('name')
        worker = request.data.get('worker')
        data = {"name": name, "worker": worker}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            tradepoint_saved = serializer.save()
        return Response({"success": "TradePoint '{}' created successfully".format(tradepoint_saved)})    

class VisitView(APIView):
    serializer_class = VisitSerializer

    def get(self, request):
        visits = Visit.objects.all()
        serializer = self.serializer_class(visits, many=True)
        return Response(serializer.data)

    def post(self, request):
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
        def get(self, request, phone_number='asdasd'):
            tradepoints = self.get_queryset()
            serializer = self.serializer_class(tradepoints, many=True)
            return Response(serializer.data)
        
        def get_queryset(self):
            phone_number = self.kwargs.get('phone_number', None)
            return TradePoint.objects.filter(worker__phone_number=phone_number)