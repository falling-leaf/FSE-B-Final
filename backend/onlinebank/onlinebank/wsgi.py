"""
WSGI config for onlinebank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from loan.manager_views import update_loan_record_isoverdue
from counteropt.cashier_views import time_deposit_record_update, demand_deposit_record_update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinebank.settings')

application = get_wsgi_application()
'''update_loan_record_isoverdue()
time_deposit_record_update()
demand_deposit_record_update()'''
