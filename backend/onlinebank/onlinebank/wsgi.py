"""
WSGI config for onlinebank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from counteropt.cashier_views import deposit_record_update
from loan.manager_views import update_loan_record_isoverdue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinebank.settings')

application = get_wsgi_application()
deposit_record_update()
update_loan_record_isoverdue()
