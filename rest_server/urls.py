from django.urls import path
from . views import VisitView, GetTradePointsByPhone

app_name = "rest-server"

urlpatterns = [
    path(r'visit/', VisitView.as_view()),
    path(r'tradepoint/<phone_number>', GetTradePointsByPhone.as_view()),
]