"""
URL configuration for onlinebank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager/', include('counteropt.manager_urls')),
    path('cashier/', include('counteropt.cashier_urls')),
    path('FExchange/', include('foreign_exchange.fe_operator_urls')),
    path('FExchange/', include('foreign_exchange.currency_urls')),
    path('FExchange/', include('foreign_exchange.fe_trading_urls')),
    path('FExchange/', include('foreign_exchange.rate_update_record_urls')),
    path('FExchange/', include('foreign_exchange.currency_holding_urls')),
    path('creditcard/', include('creditcard.urls')),
    path('login/', include('login.login_urls')),
    path('loan/', include('loan.user_urls')),
    path('loanExaminer/', include('loan.loanexaminer_urls')),
    path('loanManager/', include('loan.loanmanager_urls')),
    
    path('OBmanager/', include('bank_app.manager_urls')),
    path('user/', include('bank_app.user_urls')),
]
