from rest_framework import serializers
from . models import Worker, TradePoint, Visit

class WorkerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Worker
        fields = '__all__'
    
    def create(self, validated_data):
        return Worker.objects.create(**validated_data)

class TradePointSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePoint
        fields = '__all__'
    
    def create(self, validated_data):
        return TradePoint.objects.create(**validated_data)

class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = '__all__'
    
    def create(self, validated_data):
        return Visit.objects.create(**validated_data)
