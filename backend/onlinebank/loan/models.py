from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password, check_password
from common.models import deposit_record, withdrawal_record, transfer_record
from common.models import employee, sys_manager, online_user, account

class LoanDepartmentManager(models.Model):
    loan_manager_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(employee, on_delete=models.CASCADE, db_column="employee_id")
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    other_information = models.TextField(default="This is additional information from the loan department manager")

    class Meta:
        db_table = "loan_department_manager"
        verbose_name = "loan department manager"

    def setPassword(self, row_password):
        self.password = make_password(password=row_password)

    def checkPassword(self, row_password):
        return check_password(row_password, self.password)

class LoanExaminer(models.Model):
    loan_examiner_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(employee, on_delete=models.CASCADE, db_column="employee_id")
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    other_information = models.TextField(default="This is additional information from the loan examiner")

    class Meta:
        db_table = "loan_examiner"
        verbose_name = "loan examiner"

    def setPassword(self, row_password):
        self.password = make_password(password=row_password)

    def checkPassword(self, row_password):
        return check_password(row_password, self.password)

# The following is the data structure of the service

class LoanApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    identity_card = models.CharField(max_length=18)
    account_id = models.ForeignKey(account, on_delete=models.CASCADE, db_column="account_id")
    amount = models.FloatField()
    application_data = models.DateTimeField(auto_now_add=True)
    loan_duration = models.IntegerField()
    status = models.CharField(max_length=100, null=True)
    remark = models.TextField(default="This is remark about the loan application")

    class Meta:
        db_table = "loan_application"
        verbose_name = "loan application"

class LoanApproval(models.Model):
    approval_id = models.AutoField(primary_key=True)
    loan_examiner_id = models.ForeignKey(LoanExaminer, on_delete=models.CASCADE, db_column="loan_examiner_id")
    application_id = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, db_column="application_id")
    result = models.BooleanField()
    approval_date = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "loan_approval"
        verbose_name = "loan approval"

class Lender(models.Model):
    lender_id = models.AutoField(primary_key=True)
    loan_manager_id = models.ForeignKey(LoanDepartmentManager, on_delete=models.CASCADE, db_column="loan_manager_id")
    application_id = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, db_column="application_id")
    result = models.BooleanField()
    lender_date = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "lender"

''' 
在放款之后产生一个贷款记录用来监控后期还款以及实现还款提醒
因此需要通过lender记录计算其end_time
'''
class LoanRecord(models.Model):
    loan_id = models.AutoField(primary_key=True)
    loan_examiner_id = models.ForeignKey(LoanExaminer, on_delete=models.CASCADE, db_column="loan_examiner_id")
    loan_manager_id = models.ForeignKey(LoanDepartmentManager, on_delete=models.CASCADE, db_column="loan_manager_id")
    application_id = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, db_column="application_id")
    effective_date = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    is_repay = models.BooleanField(default=False)
    remark = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "loan_record"
        verbose_name = "loan record"

    def setEndTime(self, loan_duration):
        self.end_time = self.effective_date + relativedelta(months=loan_duration)

class LoanRepayment(models.Model):
    repayment_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(LoanRecord, on_delete=models.CASCADE, db_column="loan_id")
    repayment_date = models.DateTimeField(auto_now_add=True)
    is_overdue = models.BooleanField(default=False)
    remark = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "loan_repayment"
        verbose_name = "loan repayment"