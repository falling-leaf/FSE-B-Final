from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import JsonResponse
from . import models
import datetime
import json

@csrf_exempt
def showAllLoanApplicationUnapproved(request):
    ''' 贷款审核员界面显示所有未审批的贷款申请 '''

    response = {}
    try:
        loan_approvals = models.LoanApproval.objects.all()
        # exclude remove those that meet the conditions, __in indicates that it exists in its list
        unapproved_applications = models.LoanApplication.objects.exclude(
            application_id__in=loan_approvals.values_list('application_id', flat=True)
        )

        # 2024.6.3 添加一个信息显示该信用卡已贷但未还的金额
        unapproved_application_list = []
        for unapproved_application in unapproved_applications:
            unapproved_application_map = {}
            account_id = unapproved_application.account_id_id
            loan_applications = models.LoanApplication.objects.filter(account_id=account_id, status="待还款")
            lentMoney = 0
            for loan_application in loan_applications:
                lentMoney += loan_application.amount
            account = models.Account.objects.get(account_id=unapproved_application.account_id_id)
            account.lent_money = lentMoney
            account.save()

            unapproved_application_map['identity_card'] = unapproved_application.identity_card
            unapproved_application_map['account_id'] = unapproved_application.account_id_id
            unapproved_application_map['amount'] = unapproved_application.amount
            unapproved_application_map['loan_duration'] = unapproved_application.loan_duration
            unapproved_application_map['application_data'] = str(unapproved_application.application_data)
            unapproved_application_map['credit_limit'] = account.credit_limit
            unapproved_application_map['lent_money'] = account.lent_money
            unapproved_application_map['application_id'] = unapproved_application.application_id
            unapproved_application_list.append(unapproved_application_map)

        print(unapproved_application_list)

        response['response_code'] = 1
        response['response_message'] = "Find all unapproved loan records"
        response['unapproved_application_list'] = unapproved_application_list
    except Exception as e:
        response['response_code'] = 0
        response['response_message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(['POST'])
def approvalLoanApplication(request):
    ''' 贷款审核员审批贷款申请 '''

    response = {}
    with transaction.atomic():
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            result = body.get("result")
            loan_examiner_id = body.get("loan_examiner_id")
            application_id = body.get("application_id")
            print(result, loan_examiner_id, application_id)
            loan_examiner = models.LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)

            if models.LoanApproval.objects.filter(application_id=application_id).exists():
                raise Exception("Error! The loan application has been approved!")
            loan_application = models.LoanApplication.objects.get(application_id=application_id)

            models.LoanApproval.objects.create(
                loan_examiner_id=loan_examiner,
                application_id=loan_application,
                result=result,
                remark="This is remark about the loan approval"
            )

            response['response_code'] = 1
            response['response_message'] = f"The loan examiner{loan_examiner_id} approves the loan application{application_id} and the structure is {result}"
        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
def showAllLoanApplicationUnlent(request):
    ''' 贷款部门经理界面显示所有未放款的已审批通过的贷款记录 '''

    response = {}
    try:
        loan_approvals = models.LoanApproval.objects.filter(result=True)
        lenders = models.Lender.objects.all()
        # The judgment conditions have been approved and the loan has not been disbursed
        unlent_approvals = loan_approvals.exclude(
            application_id__in=lenders.values_list('application_id', flat=True)
        )

        unlent_approval_list = []
        for unlent_approval in unlent_approvals:
            unlent_approval_map = {}
            loan_application = models.LoanApplication.objects.get(application_id=unlent_approval.application_id_id)
            unlent_approval_map['identity_card'] = loan_application.identity_card
            unlent_approval_map['account_id'] = loan_application.account_id_id
            unlent_approval_map['amount'] = loan_application.amount
            unlent_approval_map['loan_duration'] = loan_application.loan_duration
            unlent_approval_map['approval_id'] = unlent_approval.approval_id
            unlent_approval_list.append(unlent_approval_map)

            print(unlent_approval_list)

        response['response_code'] = 1
        response['response_message'] = "Query the loan records of all pending loans"
        response['unlent_approval_list'] = unlent_approval_list
    except Exception as e:
        response['response_code'] = 0
        response['response_message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(['POST'])
def lenderLoanApplication(request):
    ''' 贷款部门经理放款 '''

    response = {}
    with transaction.atomic():
        try:
            print(request.body)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            loan_manager_id = body.get("loan_manager_id")
            approval_id = body.get("approval_id")
            result = body.get("result")
            print(loan_manager_id, approval_id, result)
            loan_manager = models.LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)
            loan_approval = models.LoanApproval.objects.get(approval_id=approval_id)
            application_id = loan_approval.application_id_id
            loan_application = models.LoanApplication.objects.get(application_id=application_id)
            print(1)

            if models.Lender.objects.filter(application_id=application_id).exists() or models.LoanRecord.objects.filter(application_id=application_id).exists():
                raise Exception("Error! The loan application has been lent!")

            '''
            放款的步骤为:生成放款记录，生成贷款记录，给用户卡号余额添加amount
            '''
            print(2)
            models.Lender.objects.create(
                loan_manager_id=loan_manager,
                application_id=loan_application,
                result=result,
                remark="This is remark about the lender"
            )
            print(3)

            now_time = datetime.datetime.now()
            loan_record = models.LoanRecord(
                loan_examiner_id=loan_approval.loan_examiner_id,
                loan_manager_id=loan_manager,
                application_id=loan_application,
                effective_date=now_time,
                remark="This is remark about the loan record"
            )
            loan_record.setEndTime(loan_application.loan_duration)
            loan_record.save()
            print(4)

            account = models.account.objects.get(account_id=loan_application.account_id_id)
            # 等待函数change_balance
            account.balance += loan_application.amount
            account.uncredited_deposit += loan_application.amount
            account.save()
            print(5)

            response['response_code'] = 1
            response['response_message'] = f"The loan application{application_id} was issued by the loan department manager{loan_manager_id}" \
                                           f" and the result was {result}.At the same time, a loan record{loan_record.loan_id} is generated"
        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)

    return JsonResponse(response)