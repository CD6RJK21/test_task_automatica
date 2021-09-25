from django.urls import path
from . views import TradePointView, VisitView, WorkerView, GetTradePointsByPhone

app_name = "rest-server"

urlpatterns = [
    path(r'tradepoint/', TradePointView.as_view()),
    path(r'visit/', VisitView.as_view()),
    path(r'worker/', WorkerView.as_view()),
    path(r'tradepoint/<phone_number>', GetTradePointsByPhone.as_view()),
]