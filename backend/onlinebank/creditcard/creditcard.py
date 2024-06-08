# from django.core.exceptions import ObjectDoesNotExist
# from ..counteropt.models import employee, online_user
#
# from models import CreditCard, CreditCardExaminer, CreditCardApplication, Transaction
#
#
# def add_credit_examiner(employee_id):
#     try:
#         Employee = employee.objects.get(employee_id=employee_id)
#         if CreditCardExaminer.objects.filter(employee=Employee).exists():
#             raise ValueError("该员工已经是信用卡审查员")
#
#         # create a new CreditCardExaminer
#         new_examiner = CreditCardExaminer(
#             employee=Employee,
#             account=Employee.identity_card,  # Example account name generation
#             password='password',
#             check_authority=1  # default grant the authority
#         )
#         new_examiner.save()
#         return new_examiner
#
#     except ObjectDoesNotExist:
#         raise ValueError("该员工不存在")
#
#
# def modify_examiner_info(self, new_account, new_password):
#     """更改审核员账号信息"""
#     # new account is same as others account, not allow
#     if not self.account == new_account and CreditCardExaminer.objects.filter(account=new_account).exists():
#         raise ValueError("该账号已存在（被他人占用）")
#     else:
#         self.account = new_account
#     # new password is the same as the old one, not allow
#     if self.password == new_password:
#         raise ValueError("新密码不能和旧密码相同")
#     else:
#         self.password = new_password
#         self.save()
#
#
# def grant(self):
#     if self.check_authority:
#         raise ValueError("该员工已被授权，无法重复授权")
#     else:
#         self.check_authority = True
#
#
# def revoke(self):
#     if not self.check_authority:
#         raise ValueError("该员工无权限，无法收回权限")
#     else:
#         self.check_authority = False
#
#
# def new_card(online_user_id):
#     ## 需要加上更具不同的信用额度来判断
#     new_card = CreditCard()
#     new_card.online_user = online_user.objects.get(person_id=online_user_id)
#     new_card.save()
#     return new_card
#
#
# def modify_password(self, new_password, old_password):
#     """更改信用卡密码，输入新密码"""
#     if old_password != self.password:
#         raise ValueError("密码不匹配")
#     elif new_password == self.password:
#         raise ValueError("新密码与旧密码相同")
#     elif self.is_lost:
#         raise ValueError("此卡已挂失")
#     elif self.is_frozen:
#         raise ValueError("此卡已冻结")
#     self.password = new_password
#     self.save()
#
#
# def report_lost(self, password):
#     """挂失信用卡，并自动冻结卡"""
#     if password != self.password:
#         raise ValueError("密码不匹配")
#     elif self.is_lost:
#         raise ValueError("此卡已挂失")
#     elif self.is_frozen:
#         raise ValueError("此卡已冻结")
#     else:
#         self.is_lost = True
#         self.is_frozen = True
#         self.save()
#         return True
#
#
# def want_cancel_card(self, password):
#     """取消信用卡，删除记录"""
#     if password != self.password:
#         raise ValueError("密码不匹配")
#     self.delete()
#     return True
#
#
# def update_credit_limit(self, password, amount):
#     """更新信用额度"""
#     if password != self.password:
#         raise ValueError("密码不匹配")
#     elif self.is_lost or self.is_frozen:
#         raise ValueError("无法更新额度，此卡已挂失或冻结")
#     elif not self.check_card():
#         raise ValueError("信用卡已透支，请还款后再申请更新额度")
#     else:
#         self.credit_limit = amount
#         self.save()
#         return True
#
#
# def report_frozen(self, password):
#     """冻结信用卡"""
#     if password != self.password:
#         raise ValueError("密码不匹配")
#     elif self.is_frozen:
#         raise ValueError("此卡已冻结")
#     else:
#         self.is_frozen = True
#         self.save()
#         return True
#
#
# def card_repay(self, pay_account, pay_password, amount):
#     if self.is_frozen or self.is_lost:
#         raise ValueError("当前信用卡已被冻结或挂失")
#     elif pay_account.password != pay_password:
#         raise ValueError("还款账户密码错误")
#     elif self.account_id == pay_account.account_id:
#         raise Warning("还款账户与当前账户不能一样")
#     elif pay_account.is_frozen or pay_account.is_lost:
#         raise ValueError("还款账户已被被冻结或挂失，不能还款")
#     elif pay_account.balance < amount:
#         raise ValueError("还款账户余额不足（还款不能透支信用）")
#     elif self.balance >= 0:
#         raise Warning("账户无需还款，余额≥0")
#     else:
#         pay_account.balance -= amount
#         self.balance += amount
#         self.save()
#         pay_account.save()
#
#
# def transfer_in(self, delta):
#     # 转入金额
#     if self.is_frozen or self.is_lost:
#         raise ValueError("信用卡已被冻结或挂失")
#     else:
#         self.balance += delta
#         self.save()
#
#
# def transfer_out(self, delta, password):
#     # 转出金额
#     if self.is_frozen or self.is_lost:
#         raise ValueError("已冻结或挂失")
#     elif self.password != password:
#         raise ValueError("密码错误")
#     elif self.balance + self.credit_limit < delta:
#         raise ValueError("余额不足")
#     else:
#         self.balance -= delta
#         self.save()
#
#
# def check_card(self):
#     if self.balance < - self.credit_limit:
#         self.is_frozen = True
#         self.save()
#         return False
#     return True
#
#
# def new_apply(online_user_id):
#     # query is exists non-check application
#     exist = CreditCardApplication.objects.filter(online_user=online_user_id, apply_status=False).exists()
#     if exist:
#         raise ValueError("您有未审核的申请，请不要重复提交")
#     new_application = CreditCardApplication()
#     new_application.online_user = online_user.objects.get(person_id=online_user_id)
#     new_application.save()
#     return new_application
#
#
# def change_state(self, apply_result, credit_examiner_id):
#     self.apply_status = True
#     self.apply_result = apply_result
#     self.credit_examiner_id = credit_examiner_id
#     self.save()
#
#
# def get_state(self):
#     try:
#         application = CreditCardApplication.objects.get(apply_id=self.apply_id)
#         if application.apply_status:
#             return application.apply_result
#         else:
#             return "申请还在审核中"
#     except CreditCardApplication.DoesNotExist:
#         raise ValueError("未找到该申请")
