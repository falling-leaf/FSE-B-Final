import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from common.models import cashier, sys_manager
from django.views.decorators.csrf import csrf_exempt
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
        rs = []
        rs.append(rs_dict)
        return JsonResponse(rs, safe = False)
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
