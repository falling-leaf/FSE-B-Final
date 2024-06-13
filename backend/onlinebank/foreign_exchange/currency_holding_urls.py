from django.urls import path, re_path
from foreign_exchange import currency_holding_views

urlpatterns = [
    re_path('user/holding', currency_holding_views.get_currency_holding),
    re_path('user/currency/amount', currency_holding_views.confirm_currency_holding),
    re_path('user/account', currency_holding_views.get_accounts),
    re_path('user/currency_holding/update', currency_holding_views.update_holding),
]