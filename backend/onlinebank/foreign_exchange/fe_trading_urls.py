from django.urls import path, re_path
from foreign_exchange import fe_trading_views

urlpatterns = [
    re_path('user/history/get', fe_trading_views.get_histories),
    re_path('history/add', fe_trading_views.add_trading_history),
    re_path('user/account/sell', fe_trading_views.currency_transfer_in),
    re_path('user/account/buy', fe_trading_views.currency_transfer_out),
    re_path('user/getname', fe_trading_views.get_user_account_name),
]