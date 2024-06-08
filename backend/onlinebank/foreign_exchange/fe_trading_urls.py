from django.urls import path, re_path
from foreign_exchange import fe_trading_views

urlpatterns = [
    re_path('user/currency/sell', fe_trading_views.createTradeData),
    re_path('user/history/get', fe_trading_views.get_histories)
]