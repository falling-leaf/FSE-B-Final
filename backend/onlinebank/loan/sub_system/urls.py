from django.urls import path  
from . import views  

urlpatterns = [
    path('manage_loan_examiner/', views.manageLoanExaminer, name='manage_loan_examiner'),
    path('manage_loan_department_manager/', views.manageLoanDepartmentManager, name='manage_loan_department_manager'),
]