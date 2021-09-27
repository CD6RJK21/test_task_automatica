from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



class Worker(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone_number = PhoneNumberField(null=False,verbose_name='Телефон', blank=False, unique=True)

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

    class Meta:
        read_only_model = True
        
    def __str__(self):
        return '|'.join([str(self.date) + str(self.place)])