from django.urls import path, re_path
from foreign_exchange import currency_holding_views

urlpatterns = [
    re_path('user/holding', currency_holding_views.get_currency_holding),
]