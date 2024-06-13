from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from common.models import cashier, sys_manager, ForeignExchangeOperator, CreditCardExaminer
from common.models import LoanExaminer, LoanDepartmentManager, online_user
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def login_sysManager(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        check_psw = data.get("password")
        sys_managers = sys_manager.objects.all()
        sys_manager_list = list(sys_managers.values())
        Has_account = False
        check_id = -1
        for one_manager in sys_manager_list:
            if one_manager["account"] == check_account:
                Has_account = True
                if one_manager["password"] == check_psw:
                    check_id = one_manager["sys_manager_id"]
                    break
        if not Has_account:
            return JsonResponse({"error": "账户不存在"}, status=403)
        if check_id == -1:
            return JsonResponse({"error": "密码错误"}, status = 403)
        rs_dict = {}
        rs_dict["id"] = check_id
        return JsonResponse(rs_dict, safe = False)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)


@csrf_exempt
def login_cashier(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        check_psw = data.get("password")
        cashiers = cashier.objects.all()
        cashier_list = list(cashiers.values())
        Has_account = False
        check_id = -1
        for one_cashier in cashier_list:
            if one_cashier["account"] == check_account:
                Has_account = True
                if one_cashier["password"] == check_psw:
                    check_id = one_cashier["cashier_id"]
                    break
        if not Has_account:
            return JsonResponse({"error":"账户不存在"}, status=403)
        if check_id == -1:
            return JsonResponse({"error": "密码错误"}, status=403)
        rs_dict = {}
        rs_dict["id"] = check_id
        return JsonResponse(rs_dict, safe = False)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def login_feOperator(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        check_psw = data.get("password")
        operators = ForeignExchangeOperator.objects.all()
        operators_list = list(operators.values())
        Has_account = False
        check_id = -1
        for o in operators_list:
            if o["account"] == check_account:
                Has_account = True
                if o["password"] == check_psw:
                    check_id = o["foreign_exchange_operator_id"]
                    break
        if not Has_account:
            return JsonResponse({"error":"账户不存在"}, status=403)
        if check_id == -1:
            return JsonResponse({"error": "密码错误"}, status=403)
        rs_dict = {}
        rs_dict["id"] = check_id
        return JsonResponse(rs_dict, safe = False)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)
    
@csrf_exempt
def login_creditexmainer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        check_psw = data.get("password")
        creditcardExaminer = CreditCardExaminer.objects.all()
        operators_list = list(creditcardExaminer.values())
        Has_account = False
        check_id = -1
        for o in operators_list:
            if o["account"] == check_account:
                Has_account = True
                if o["password"] == check_psw:
                    check_id = o["credit_examiner_id"]
                    break
        if not Has_account:
            return JsonResponse({"error":"账户不存在"}, status=403)
        if check_id == -1:
            return JsonResponse({"error": "密码错误"}, status=403)
        rs_dict = {}
        rs_dict["id"] = check_id
        return JsonResponse(rs_dict, safe = False)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
@require_http_methods(["POST"])
def loanExaminerLogin(request):
    ''' 贷款部门审查员登录 '''
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print(body_unicode)
        check_account = body.get('account')
        password = body.get('password')
        loan_examiner_account = LoanExaminer.objects.get(account=check_account)
        if loan_examiner_account.checkPassword(password):
            print(1)
            return JsonResponse({"loan_examiner_id": loan_examiner_account.loan_examiner_id})
        else:
            return JsonResponse({"error": "密码错误"}, status=403)
    except LoanExaminer.DoesNotExist:
        return JsonResponse({"error": "该用户不存在"}, status=403)
    except LoanExaminer.MultipleObjectsReturned:
        return JsonResponse({"error": "用户名重叠"}, status=403)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=403)


@csrf_exempt
@require_http_methods(["POST"])
def loanDepartmentManagerLogin(request):
    ''' 贷款部门经理登录 '''
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        check_account = body.get('account')
        password = body.get('password')
        loan_manager_account = LoanDepartmentManager.objects.get(account=check_account)
        if loan_manager_account.checkPassword(password):
            return JsonResponse({"loan_manager_id": loan_manager_account.loan_manager_id})
        else:
            return JsonResponse({"error": "密码错误"}, status=403)
    except LoanExaminer.DoesNotExist:
        return JsonResponse({"error": "该用户不存在"}, status=403)
    except LoanExaminer.MultipleObjectsReturned:
        return JsonResponse({"error": "用户名重叠"}, status=403)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=403)


@csrf_exempt
@require_http_methods(["POST"])
def getUserIdentityCard(request):
    ''' 跳转到贷款模块获取用户身份码 '''
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        user_id = body.get('user_id')
        user = online_user.objects.get(user_id=user_id)
        return JsonResponse({'identity_card': user.identity_card}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)