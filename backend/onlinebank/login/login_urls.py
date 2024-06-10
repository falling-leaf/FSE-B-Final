from django.urls import path
from . import login_views

urlpatterns = [
    path('sysManager/', login_views.login_sysManager),
    path('cashier/', login_views.login_cashier),
    path('FEOperator/', login_views.login_feOperator),
    path('creditcardExmainer/',login_views.login_creditexmainer),
]