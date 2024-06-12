from . import manager_views
from django.urls import path

urlpatterns = [
    path('showAllLoanApplicationUnapproved', manager_views.showAllLoanApplicationUnapproved, name='show_all_loan_application_unapproved'),
    path('approvalLoanApplication', manager_views.approvalLoanApplication, name='approval_loan_application'),
]