from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=20, null=False, default="Unknown")
    identity_card = models.CharField(max_length=18, null=False, default="Unknown")
    employee_sex = models.IntegerField(null=False, default=0)
    phone_number = models.CharField(max_length=20, null=False, default="Unknown")
    occupation_name = models.CharField(max_length=50, null=False, default="Unknown")
    is_employeed = models.BooleanField(null=False, default="False")
    other_information = models.CharField(max_length=1021, default="Unknown")


class sys_manager(models.Model):
    sys_manager_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=20, null=False)


class cashier(models.Model):
    cashier_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=20, null=False)
    trade_authority = models.BooleanField(null=False)
    manage_authority = models.BooleanField(null=False)


class online_bank_manager(models.Model):
    online_bank_manager_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=20, null=False)


class online_user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, null=False, default="Unknown")
    password = models.CharField(max_length=20, null=False, default="666666")
    identity_card = models.CharField(max_length=18, null=False, unique=True)
    phone_num = models.CharField(max_length=20, null=False, default="10086")
    annual_income = models.FloatField(null=True)
    property_valuation = models.FloatField(null=True)
    service_year = models.IntegerField(null=True)
    is_frozen = models.BooleanField(null=False, default=False)
    is_lost = models.BooleanField(null=False, default=False)
    is_blacklisted = models.BooleanField(default=False)


# 账户表
class account(models.Model):
    account_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20, null=False)
    user_id = models.ForeignKey(online_user, on_delete=models.SET_NULL, related_name="accounts", null=True)
    identity_card = models.CharField(max_length=18, null=False)
    phone_num = models.CharField(max_length=20, null=False, default="10086")
    card_type = models.IntegerField(null=False)
    balance = models.FloatField(null=False, default=0.0)
    current_deposit = models.FloatField(null=False, default=0.0)
    uncredited_deposit = models.FloatField(null=False, default=0.0)
    credit_limit = models.FloatField(default=10000)
    lent_money = models.FloatField(null=True)
    is_frozen = models.BooleanField(null=False, default=False)
    is_lost = models.BooleanField(null=False, default=False)
    open_date = models.DateTimeField(default=timezone.now)  # Automatically set to today's date as default
    uncredited_deposit_update_date = models.DateTimeField(null=False, default=timezone.now)

    @staticmethod
    def new_card(online_user_id, card_type):
        new_card = account()
        new_card.online_user = online_user.objects.get(person_id=online_user_id)
        new_card.account_type = card_type
        new_card.save()
        return new_card

    def modify_password(self, new_password, old_password):
        """更改信用卡密码，输入新密码"""
        if old_password != self.password:
            raise ValueError("密码不匹配")
        elif new_password == self.password:
            raise ValueError("新密码与旧密码相同")
        elif self.is_lost:
            raise ValueError("此卡已挂失")
        elif self.is_frozen:
            raise ValueError("此卡已冻结")
        self.password = new_password
        self.save()

    def report_lost(self, password):
        """挂失信用卡，并自动冻结卡"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_lost:
            raise ValueError("此卡已挂失")
        elif self.is_frozen:
            raise ValueError("此卡已冻结")
        else:
            self.is_lost = True
            self.is_frozen = True
            self.save()
            return True

    def cancel_card(self, password):
        """取消信用卡，删除记录"""
        if password != self.password:
            raise ValueError("密码不匹配")
        self.delete()
        return True

    def update_credit_limit(self, password):
        """更新信用额度"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_lost or self.is_frozen:
            raise ValueError("无法更新额度，此卡已挂失或冻结")
        elif not self.check_card():
            raise ValueError("信用卡已透支，请还款后再申请更新额度")
        else:
            loan_records = LoanRecord.objects.all()
            for loan_record in loan_records:
                if loan_record.is_overdue:
                    self.credit_limit = 0
                    self.save()
            # 获取卡对应user的财产信息以及该卡的存取转账信息
            user = online_user.objects.get(identity_card=self.identity_card)
            deposit_records = deposit_record.objects.filter(account_id=self.account_id)
            withdrawal_records = withdrawal_record.objects.filter(account_id=self.account_id)
            transfer_in_records = transfer_record.objects.filter(account_in_id=self.account_id)
            transfer_out_records = transfer_record.objects.filter(account_out_id=self.account_id)
            total_income = sum(record.deposit_amount for record in deposit_records) + sum(
                record.transfer_amount for record in transfer_in_records)
            income_frequency = deposit_records.count() + transfer_in_records.count()
            total_outcome = sum(record.withdrawal_amount for record in withdrawal_records) + sum(
                record.transfer_amount for record in transfer_out_records)
            outcome_frequency = withdrawal_records.count() + transfer_out_records.count()

            annual_income_parameter = 0
            if user.service_year is None or user.service_year == 0:
                annual_income_parameter = 0
            elif user.service_year <= 20:
                annual_income_parameter = user.service_year / 20.0
            else:
                annual_income_parameter = 1

            # 一般转入频率低而转出频率高，需要对转出的数据进行补偿
            credit_limit = user.property_valuation + user.annual_income * annual_income_parameter * 0.5 + (
                        total_income * 0.1 / income_frequency - total_outcome * 0.8 / outcome_frequency) * 450

            self.credit_limit = credit_limit
            self.save()

    def frozen_card(self, password):
        """冻结信用卡"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_frozen:
            raise ValueError("此卡已冻结")
        else:
            self.is_frozen = True
            self.save()
            return True

    def repay(self, pay_account, pay_password, amount):
        if self.is_frozen or self.is_lost:
            raise ValueError("当前信用卡已被冻结或挂失")
        elif pay_account.password != pay_password:
            raise ValueError("还款账户密码错误")
        elif self.account_id == pay_account.account_id:
            raise Warning("还款账户与当前账户不能一样")
        elif pay_account.is_frozen or pay_account.is_lost:
            raise ValueError("还款账户已被被冻结或挂失，不能还款")
        elif pay_account.balance < amount:
            raise ValueError("还款账户余额不足（还款不能透支信用）")
        elif self.balance >= 0.0:
            raise Warning("账户无需还款，余额≥0")
        else:
            pay_account.balance -= amount
            self.balance += amount
            self.save()
            pay_account.save()

    def transfer_in(self, delta):
        # 转入金额
        if self.is_frozen or self.is_lost:
            raise ValueError("信用卡已被冻结或挂失")
        else:
            self.balance += delta
            self.save()

    def transfer_out(self, delta, password):
        # 转出金额
        if self.is_frozen or self.is_lost:
            raise ValueError("已冻结或挂失")
        elif self.password != password:
            raise ValueError("密码错误")
        elif self.balance + self.credit_limit < delta:
            raise ValueError("余额不足")
        else:
            self.balance -= delta
            self.save()

    def check_card(self):
        if self.balance < - self.credit_limit:
            self.is_frozen = True
            self.save()
            return False
        return True


class BlackList(models.Model):
    list_id = models.AutoField(primary_key=True)
    online_bank_manager_id = models.ForeignKey(online_bank_manager, on_delete=models.CASCADE, default=1,
                                               db_column='online_bank_manager_id')
    user_id = models.ForeignKey(online_user, on_delete=models.CASCADE, db_column='user_id')
    timestamp = models.DateTimeField(auto_now_add=True)


# 存款记录
class deposit_record(models.Model):
    deposit_record_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(null=False)
    deposit_type = models.CharField(max_length=10, null=False)
    auto_renew_status = models.BooleanField(null=True)
    deposit_start_date = models.DateField(null=False)
    # 新增更新时间
    deposit_update_date = models.DateField(null=False)
    deposit_end_date = models.DateField(null=True)
    deposit_amount = models.FloatField(null=False)
    cashier_id = models.IntegerField(null=False)


# 取款记录
class withdrawal_record(models.Model):
    withdrawal_record_id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(null=False)
    withdrawal_date = models.DateField(null=False)
    withdrawal_amount = models.FloatField(null=False)
    cashier_id = models.IntegerField(null=False)


# 转账记录
class transfer_record(models.Model):
    transfer_record_id = models.AutoField(primary_key=True)
    account_in_id = models.IntegerField(null=False)
    account_out_id = models.IntegerField(null=False)
    transfer_date = models.DateField(null=False)
    transfer_amount = models.FloatField(null=False)
    cashier_id = models.IntegerField(null=False)


# 信用卡审查员
class CreditCardExaminer(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    credit_examiner_id = models.AutoField(primary_key=True)
    check_authority = models.BooleanField(default=False)
    account = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=20, null=False)

    def modify_examiner_info(self, new_account, new_password):
        """更改审核员账号信息"""
        # new account is same as others account, not allow
        if not self.account == new_account and CreditCardExaminer.objects.filter(account=new_account).exists():
            raise ValueError("该账号已存在（被他人占用）")
        else:
            self.account = new_account
        # new password is the same as the old one, not allow
        if self.password == new_password:
            raise ValueError("新密码不能和旧密码相同")
        else:
            self.password = new_password

        self.save()

    def grant(self):
        if self.check_authority:
            raise ValueError("该员工已被授权，无法重复授权")
        else:
            self.check_authority = True

    def revoke(self):
        if not self.check_authority:
            raise ValueError("该员工无权限，无法收回权限")
        else:
            self.check_authority = False


# 申请记录
class CreditCardApplication(models.Model):
    apply_id = models.AutoField(primary_key=True)
    online_user = models.ForeignKey(online_user, on_delete=models.CASCADE)
    creditCardExaminer = models.ForeignKey(CreditCardExaminer, on_delete=models.CASCADE, null=True, default=None)
    apply_status = models.BooleanField(default=False)
    apply_result = models.BooleanField(default=False)
    apply_date = models.DateTimeField(default=timezone.now)
    have_open = models.BooleanField(default=False)

    DEFAULT_CREDIT_LIMIT = 1000.0  # 默认信用额度

    @staticmethod
    def new_apply(online_user_id):
        # query is exists non-check application
        exist = CreditCardApplication.objects.filter(online_user=online_user_id, apply_status=False).exists()
        if exist:
            raise ValueError("您有未审核的申请，请不要重复提交")
        new_application = CreditCardApplication()
        new_application.online_user = online_user.objects.get(user_id=online_user_id)
        new_application.save()
        return new_application

    def change_state(self, apply_result, credit_examiner_id):
        self.apply_status = True
        self.apply_result = apply_result
        self.credit_examiner_id = credit_examiner_id
        self.save()

    def get_state(self):
        try:
            application = CreditCardApplication.objects.get(apply_id=self.apply_id)
            if application.apply_status:
                return application.apply_result
            else:
                return "申请还在审核中"
        except CreditCardApplication.DoesNotExist:
            raise ValueError("未找到该申请")


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
    employee = models.ForeignKey('common.employee', on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null=False, unique=True)
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
    is_overdue = models.BooleanField(default=False)
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
    remark = models.TextField(null=True)
    objects = models.Manager()

    class Meta:
        db_table = "loan_repayment"
        verbose_name = "loan repayment"