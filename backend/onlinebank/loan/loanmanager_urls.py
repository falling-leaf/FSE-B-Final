from . import manager_views
from django.urls import path

urlpatterns = [
    path('showAllLoanApplicationUnlent', manager_views.showAllLoanApplicationUnlent, name='show_all_loan_application_unlent'),
    path('lenderLoanApplication', manager_views.lenderLoanApplication, name='lender_loan_application'),
    path('unrepayReminderManager', manager_views.unrepayReminderManager),
]

from . import models
from django.db import transaction
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore, register_job
from apscheduler.schedulers.background import BackgroundScheduler

''' scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(
#     scheduler, 'cron', hour="*/12", minute='0', second='0',
#     replace_existing=True, timezone='Asia/Shanghai',
#     id="update_loan_record_isoverdue"
#     )
# def update_loan_record_isoverdue():
#     with transaction.atomic():
#         try:
#             loan_records = LoanRecord.objects.filter(is_repay=False)
#             current_time = timezone.now()
#             for loan_record in loan_records:
#                 if loan_record.end_time < current_time:
#                     loan_record.is_overdue = True
#         except Exception as e:
#             print(str(e))

scheduler.start() '''