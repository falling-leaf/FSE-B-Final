from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from . import models
import datetime
import json

@csrf_exempt
@require_http_methods(["POST"])
def commitLoanApplication(request):
    ''' 用户提交贷款申请 '''

    response = {}
    with transaction.atomic():
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            identity_card = body.get('identity_card')
            account_id = body.get('account_id')
            amount = body.get('amount')
            loan_duration = body.get('loan_duration')
            # print(identity_card, account_id, amount, loan_duration)

            remark = "This is remark about the loan application"
            if body.get('remark') is not None:
                remark = body.get('remark')

            # There may be models.DoesNotExist errors
            check_account = models.account.objects.get(account_id=account_id)
            if check_account.card_type != 1:
                raise Exception("Error! It is not possible to borrow a loan without a credit card")
            if identity_card != check_account.identity_card:
                raise Exception("Error! The owner of the card number is not you!")

            models.LoanApplication.objects.create(identity_card=identity_card, account_id=check_account,
                                                  amount=amount, loan_duration=loan_duration, remark=remark)

            response['response_code'] = 1
            response['response_message'] = "Loan application commit successfully, the apllication date is " + str(
                datetime.datetime.now())
        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)
            print("Error!" + str(e))

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(['POST'])
def searchAllNeedRepayLoanRecord(request):
    ''' 用户查询所有需要还款的贷款 '''

    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        identity_card = body.get('identity_card')
        user = models.online_user.objects.get(identity_card=identity_card)
        accounts = models.account.objects.filter(card_type=1, identity_card=user.identity_card)
        loan_applications = models.LoanApplication.objects.filter(
            account_id__in=accounts.values_list('account_id', flat=True)
        )
        loan_records = models.LoanRecord.objects.filter(
            application_id__in=loan_applications.values_list('application_id', flat=True)
        )

        loan_records = loan_records.filter(is_repay=False)

        loan_record_list = []
        for loan_record in loan_records:
            loan_record_map = {}
            loan_record_map['loan_id'] = loan_record.loan_id
            loan_application = models.LoanApplication.objects.get(application_id=loan_record.application_id_id)
            loan_record_map['account_id'] = loan_application.account_id_id
            loan_record_map['amount'] = loan_application.amount
            loan_record_map['end_time'] = str(loan_record.end_time)
            loan_record_list.append(loan_record_map)
        print(loan_record_list)

        response['response_code'] = 1
        response['response_message'] = "Check the records of all loans that need to be repaid successfully"
        response['loan_application_list'] = loan_record_list
    except Exception as e:
        response['response_code'] = 0
        response['response_message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(['POST'])
def unrepayLoanRecordReminder(request):
    ''' 用户贷款还款提醒 '''

    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        identity_card = body.get("identity_card")
        accounts = models.account.objects.filter(identity_card=identity_card)
        loan_applications = models.LoanApplication.objects.filter(
            account_id__in=accounts.values_list("account_id", flat=True)
        )
        loan_records = models.LoanRecord.objects.filter(
            application_id__in=loan_applications.values_list("application_id", flat=True)
        )

        count = 0
        current_time = timezone.now()
        for record in loan_records:
            if current_time < record.end_time < current_time + datetime.timedelta(days=7):
                count += 1

        response['response_code'] = 1
        response['response_message'] = f"You have a record of {count} loans that need to be repaid within 7 days"
    except Exception as e:
        response['response_code'] = 0
        response['response_message'] = str(e)
        print(str(e))

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(['POST'])
def searchAllLoanApplicationByUser(request):
    ''' 用户贷款查询界面返回其所有的贷款记录 '''

    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        identity_card = body.get('identity_card')
        print(identity_card)
        loan_applications = models.LoanApplication.objects.filter(identity_card=identity_card)

        '''
        add a feature named stauts, the status has six possible values:
        待审核、审核拒绝、待放款、拒绝放款、待还款和已还款
        '''

        loan_application_list = []
        for loan_application in loan_applications:
            loan_application_map = {}
            loan_application_map['application_id'] = loan_application.application_id
            loan_application_map['account_id'] = loan_application.account_id_id
            loan_application_map['application_data'] = str(loan_application.application_data)
            loan_application_map['amount'] = loan_application.amount
            if models.LoanApproval.objects.filter(application_id=loan_application).exists():
                loan_approval = models.LoanApproval.objects.get(application_id=loan_application)

                if loan_approval.result == False:
                    loan_application.status = '审批拒绝'
                else:
                    if models.Lender.objects.filter(application_id=loan_application).exists():
                        lender = models.Lender.objects.get(application_id=loan_application)

                        if lender.result == False:
                            loan_application.status = '拒绝放款'
                        else:
                            loan_record = models.LoanRecord.objects.get(application_id=loan_application)
                            if loan_record.is_repay:
                                loan_application.status = '已还款'
                            else:
                                loan_application.status = '待还款'
                    else:
                        loan_application.status = '待放款'

            else:
                loan_application.status = '待审批'
            loan_application.save()
            loan_application_map['status'] = loan_application.status
            loan_application_list.append(loan_application_map)

        print(loan_application_list)

        response['response_code'] = 1
        response['response_message'] = "Query all loan applications with status feature of users"
        response['loan_application_list'] = loan_application_list
    except Exception as e:
        response['response_code'] = 0
        response['response_message'] = str(e)

    return JsonResponse(response)

'''
        2024.6.3
        由于银行卡的余额计算问题
凡是设计余额变更的需要等待合并后的函数change_balance(行级锁)
        包括还款的余额判断
'''
@csrf_exempt
@require_http_methods(['POST'])
def userRepayLoanByAccount(request):
    ''' 用户使用单张银行卡还款 '''

    response = {}
    with transaction.atomic():
        try:
            print(request.body)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            identity_card = body.get('identity_card')
            account_id = body.get('account_id')
            loan_id = body.get('loan_id')
            print(identity_card, account_id, loan_id)
            loan_record = models.LoanRecord.objects.get(loan_id=loan_id)

            # determine the owner and balance of the card
            check_account = models.account.objects.get(account_id=account_id)
            if identity_card != check_account.identity_card:
                raise Exception("Error! The owner of the card number is not you!")
            amount = loan_record.application_id.amount
            # 待定修改
            if check_account.balance < amount:
                raise Exception("Error! The balance of this card is not enough to repay the loan!")

            # determine wheather is overdue, > means later
            is_overdue = False
            print(loan_record.end_time, timezone.now())
            if loan_record.end_time < timezone.now():
                is_overdue = True

            if loan_record.is_repay:
                raise Exception("Error! Repayment records already exist!")

            models.LoanRepayment.objects.create(
                loan_id=loan_record,
                remark="This is remark about the loan repayment"
            )
            # 调用函数change_balance
            check_account.transfer_out(amount)
            loan_record.is_repay = True
            loan_record.save()

            response['response_code'] = 1
            response['response_message'] = "The repayment is successful, and the credit card balance is deducted"
        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)
            print(str(e))

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def updateCreditLimit(request):
    ''' 更新用户的信用额度 '''

    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        check_account = models.account.objects.get(account_id=account_id)
        loan_records = models.LoanRecord.objects.all()
        for loan_record in loan_records:
            if loan_record.is_overdue:
                check_account.credit_limit = 0
                check_account.save()
                return JsonResponse({'message': "update successfully"}, status=200)

        # 获取卡对应user的财产信息以及该卡的存取转账信息
        user = models.online_user.objects.get(identity_card=check_account.identity_card)
        deposit_records = models.deposit_record.objects.filter(account_id=account_id)
        withdrawal_records = models.withdrawal_record.objects.filter(account_id=account_id)
        transfer_in_records = models.transfer_record.objects.filter(account_in_id=account_id)
        transfer_out_records = models.transfer_record.objects.filter(account_out_id=account_id)

        total_income = sum(record.deposit_amount for record in deposit_records) + sum(record.transfer_amount for record in transfer_in_records)
        income_frequency = deposit_records.count() + transfer_in_records.count()
        total_outcome = sum(record.withdrawal_amount for record in withdrawal_records) + sum(record.transfer_amount for record in transfer_out_records)
        outcome_frequency = withdrawal_records.count() + transfer_out_records.count()

        annual_income_parameter = 0
        if user.service_year is None or user.service_year == 0:
            annual_income_parameter = 0
        elif user.service_year <= 20:
            annual_income_parameter = user.service_year / 20.0
        else:
            annual_income_parameter = 1

        # 一般转入频率低而转出频率高，需要对转出的数据进行补偿
        per_income = 0
        per_outcome = 0
        if income_frequency != 0:
            per_income = total_income / income_frequency
        if outcome_frequency != 0:
            per_outcome = total_outcome / outcome_frequency
        credit_limit = user.property_valuation + user.annual_income * annual_income_parameter * 0.5 + (per_income * 0.1 - per_outcome * 0.8) * 450

        check_account.credit_limit = credit_limit
        check_account.save()
        return JsonResponse({'message': "update successfully"}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)