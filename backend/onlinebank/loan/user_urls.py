from . import user_views
from django.urls import path

urlpatterns = [
    path('commitLoanApplication/', user_views.commitLoanApplication, name="commit_loan_application"),
    path('searchAllNeedRepayLoanRecord/', user_views.searchAllNeedRepayLoanRecord, neme="search_all_need_repay_loan_record"),
    path('unrepayLoanRecordReminder/', user_views.unrepayLoanRecordReminder, name="unrepay_loan_record_reminder"),
    path('searchAllLoanApplicationByUser/', user_views.searchAllLoanApplicationByUser, name="search_all_loan_application_by_user"),
    path('userRepayLoanByAccount/', user_views.userRepayLoanByAccount, name="user_repay_loan_by_account"),
]