from django.urls import path, re_path
from foreign_exchange import currency_views

urlpatterns = [
    re_path('user/currency/category', currency_views.get_all_currency),
    re_path('Operator/delete', currency_views.handleDeleteCurrency),
    re_path('Operator/add',currency_views.handleAddCurrency),
    re_path('Operator/modify',currency_views.handleModifyRateCurrency),
    re_path('Operator/rename',currency_views.handleModifyNameCurrency)
]