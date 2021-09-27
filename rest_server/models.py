from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.backends import BaseBackend
from django.contrib import admin

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ['coords', 'date', 'place']

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class MyModelAdmin(ReadOnlyAdmin):
    pass


class Worker(AbstractUser):
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone_number = PhoneNumberField(null=False,verbose_name='Телефон', blank=False, unique=True)
    password = ''
    PASSWORD_FIELD = 'password'
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return '|'.join([str(self.id), self.name, str(self.phone_number)])


class TradePoint(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    worker = models.ForeignKey(Worker, verbose_name='Работник', on_delete=models.CASCADE)

    def __str__(self):
        return '|'.join([self.name + str(self.worker)])


class Visit(models.Model):
    date = models.DateTimeField(verbose_name='Дата')
    place = models.ForeignKey(TradePoint, verbose_name='Место', on_delete=models.CASCADE)
    coords = models.CharField(max_length=200, verbose_name='Координаты')

    def __str__(self):
        return '|'.join([str(self.date) + str(self.place)])