from django.contrib import admin
from .models import Worker, TradePoint, Visit

admin.site.register(Worker)
admin.site.register(TradePoint)
admin.site.register(Visit)