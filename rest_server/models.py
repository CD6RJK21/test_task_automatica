from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone_number = models.CharField(max_length=30, verbose_name='Телефон', unique=True)
    
    def __str__(self):
        return '|'.join([str(self.id), self.name, self.phone_number])


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