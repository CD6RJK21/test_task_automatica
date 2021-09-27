from django.urls import path
from . views import VisitView, GetTradePointsByPhone

app_name = "rest-server"

urlpatterns = [
    path(r'visit/', VisitView.as_view()),
    path(r'tradepoint/', GetTradePointsByPhone.as_view()),
]