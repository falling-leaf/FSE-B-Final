from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
class employee(models.Model):
    employee_id = models.AutoField(primary_key = True)
    employee_name = models.CharField(max_length = 20, null = False, default = "Unknown")
    identity_card = models.CharField(max_length = 18, null = False, default = "Unknown")
    employee_sex = models.IntegerField(null = False, default = 0)
    phone_number = models.CharField(max_length = 20, null = False, default = "Unknown")
    occupation_name = models.CharField(max_length = 50, null = False, default = "Unknown")
    is_employeed = models.BooleanField(null = False, default = "False")
    other_information = models.CharField(max_length = 1021, default = "Unknown")


class sys_manager(models.Model):
    sys_manager_id = models.AutoField(primary_key = True)
    employee = models.ForeignKey(employee, on_delete = models.CASCADE)
    account = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 20, null = False)


class cashier(models.Model):
    cashier_id = models.AutoField(primary_key = True)
    employee = models.ForeignKey(employee, on_delete = models.CASCADE)
    account = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 20, null = False)
    trade_authority = models.BooleanField(null = False)
    manage_authority = models.BooleanField(null = False)


class online_user(models.Model):
    user_id = models.AutoField(primary_key = True)
    identity_card = models.CharField(max_length = 18, null = False)
    annual_income = models.FloatField(null=True)
    property_valuation = models.FloatField(null=True)
    service_year = models.IntegerField(null=True)


# 账户表
class account(models.Model):
    account_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20, null=False)
    identity_card = models.ForeignKey(online_user, on_delete=models.PROTECT)
    card_type = models.IntegerField(null=False)
    balance = models.FloatField(null=False, default=0.0)
    current_deposit = models.FloatField(null=False, default=0.0)
    uncredited_deposit = models.FloatField(null=False, default=0.0)
    credit_limit = models.FloatField(default=10000)
    lent_money = models.FloatField(null=True)
    is_frozen = models.BooleanField(null=False, default=False)
    is_lost = models.BooleanField(null=False, default=True)


# 存款记录
class deposit_record(models.Model):
    deposit_record_id = models.AutoField(primary_key = True)
    account_id = models.IntegerField(null = False)
    deposit_type = models.CharField(max_length = 10, null = False)
    auto_renew_status = models.BooleanField(null = True)
    deposit_start_date = models.DateField(null = False)
    # 新增更新时间
    deposit_update_date = models.DateField(null=False)
    deposit_end_date = models.DateField(null = True)
    deposit_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)


# 取款记录
class withdrawal_record(models.Model):
    withdrawal_record_id = models.AutoField(primary_key = True)
    account_id = models.IntegerField(null = False)
    withdrawal_date = models.DateField(null = False)
    withdrawal_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)


# 转账记录
class transfer_record(models.Model):
    transfer_record_id = models.AutoField(primary_key = True)
    account_in_id = models.IntegerField(null = False)
    account_out_id = models.IntegerField(null = False)
    transfer_date = models.DateField(null = False)
    transfer_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)

# 外汇
class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=80, unique=True)
    latest_exchange_buying_rate = models.DecimalField(max_digits=10, decimal_places=5)
    latest_exchange_selling_rate = models.DecimalField(max_digits=10, decimal_places=5)

    @staticmethod
    def GetCurrencyName(currencyId: int):
        currency = Currency.objects.get(currency_id=currencyId)
        return currency

class CurrencyHolding(models.Model):
    currency_holding_id = models.AutoField(primary_key=True)
    currency = models.ForeignKey('common.Currency', on_delete=models.CASCADE)
    online_user = models.ForeignKey('common.online_user', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
        
    class Meta:
        unique_together = ('currency', 'online_user')

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            self.delete()
        else:
            super(CurrencyHolding, self).save(*args, **kwargs)

class ForeignExchangeOperator(models.Model):
    foreign_exchange_operator_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('common.employee',on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null = False, unique= True)
    password = models.CharField(max_length=80, null=False)
    alter_name_authority = models.BooleanField(default=False)
    alter_rate_authority = models.BooleanField(default=False)
    add_authority = models.BooleanField(default=False)
    delete_authority = models.BooleanField(default=False)

    class Meta:
        db_table = 'foreign_exchange_operator'
        ordering = ['foreign_exchange_operator_id'] 

    def __str__(self):
        return f"{self.foreign_exchange_operator_id}: {self.account}"
    
class ForeignExchangeTrading(models.Model):
    foreign_exchange_trading_id = models.AutoField(primary_key=True)
    account = models.ForeignKey('common.account', on_delete=models.CASCADE)
    online_user = models.ForeignKey('common.online_user', on_delete=models.CASCADE)
    currency = models.ForeignKey('common.Currency', on_delete=models.CASCADE)
    buy_or_sell = models.BooleanField(default=False)
    rmb_amount = models.DecimalField(max_digits=10, decimal_places=5)
    currency_amount = models.DecimalField(max_digits=10, decimal_places=5)
    trading_datetime = models.DateTimeField()

class RateUpdateRecord(models.Model):
    rate_update_record_id = models.AutoField(primary_key=True)
    currency = models.ForeignKey('common.Currency', on_delete=models.CASCADE)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=5)
    selling_rate = models.DecimalField(max_digits=10, decimal_places=5)
    update_datetime = models.DateTimeField()

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

