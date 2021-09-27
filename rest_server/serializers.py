from rest_framework import serializers
from . models import Worker, TradePoint, Visit
from dj_rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = (
            'pk',
            'phone_number',
            'name'
        )
        read_only_fields = ('pk', 'phone_number',)


class CustomRegisterSerializer(RegisterSerializer):
    phone_number = PhoneNumberField()
    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get('phone_number')
        user.save()
        return user

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
