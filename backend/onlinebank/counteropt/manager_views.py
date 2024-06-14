from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
import datetime
import json


from .models import cashier, employee
from .models import LoanDepartmentManager, LoanExaminer

# Create your views here.

def all_cashiers(request):
    if request.method == 'GET':
        # 获取所有的cashier
        cashiers = cashier.objects.all()
        # 转化为list形式
        cashier_list = list(cashiers.values())
        rs = []
        cashier_dict = {}
        for one_cashier in cashier_list:
            cashier_dict = {}
            employee_list = employee.objects.get(employee_id = one_cashier["employee_id"])
            cashier_dict["id"] = one_cashier["cashier_id"]
            cashier_dict["account"] = one_cashier["account"]
            cashier_dict["password"] = one_cashier["password"]
            cashier_dict["name"] = employee_list.employee_name
            cashier_dict["identity_card"] = employee_list.identity_card
            if employee_list.employee_sex == 0:
                cashier_dict["sex"] = "男"
            else: cashier_dict["sex"] = "女"
            cashier_dict["phone"] = employee_list.phone_number
            if one_cashier["trade_authority"]:
                cashier_dict["ifTrade"] = True
            else: cashier_dict["ifTrade"] = False
            if one_cashier["manage_authority"]:
                cashier_dict["ifManage"] = True
            else: cashier_dict["ifManage"] = False
            rs.append(cashier_dict)
        return JsonResponse(rs, safe = False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def add_cashier(request):
    if request.method == 'POST':
        # data是一个字典，可以用.get()访问键值对
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        if cashier.objects.filter(account = check_account).exists():
            return JsonResponse({"error": "出纳员账户已存在"}, status = 403)
        sex = 0
        if data.get("sex") == "男":
            sex = 0
        else: sex = 1
        new_employee = employee(employee_name = data.get("name"), 
                             identity_card = data.get("identity_card"),
                             employee_sex = sex,
                             phone_number = data.get("phone"),
                             occupation_name = "bank",
                             is_employeed = True)
        new_employee.save()
        new_cashier = cashier(employee = new_employee,
                              account = data.get("account"),
                              password = data.get("password"),
                              trade_authority = data.get("trade_authority"),
                              manage_authority = data.get("manage_authority"))
        new_cashier.save()
        return JsonResponse({"success": "出纳员添加成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def delete_cashier(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        delete_cashier = cashier.objects.get(cashier_id = data.get("id"))
        modify_employee = delete_cashier.employee
        delete_cashier.delete()
        modify_employee.is_employeed = False
        modify_employee.save()
        return JsonResponse({"success": "出纳员删除成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def modify_cashier(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_cashier = cashier.objects.get(cashier_id = data.get("id"))
        if modify_cashier.account != data.get("account"):
            if cashier.objects.filter(account = data.get("account")).exists():
                return JsonResponse({"error": "出纳员账户已存在"}, status = 403)
        modify_employee = modify_cashier.employee
        modify_employee.employee_name = data.get("name")
        modify_employee.identity_card = data.get("identity_card")
        modify_employee.phone_number = data.get("phone")
        if data.get("sex") == "男":
            modify_employee.employee_sex = 0
        else: modify_employee.employee_sex = 1
        modify_cashier.password = data.get("password")
        modify_cashier.account = data.get("account")
        modify_employee.save()
        modify_cashier.save()
        return JsonResponse({"success": "修改出纳员成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def modify_authority(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_cashier = cashier.objects.get(cashier_id = data.get("id"))
        modify_cashier.trade_authority = data.get("ifTrade")
        modify_cashier.manage_authority = data.get("ifManage")
        modify_cashier.save()
        return JsonResponse({"success": "修改出纳员权限成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def getAllLoanExaminer(request):
    ''' 显示所有贷款审查员信息 '''
    if request.method == 'GET':
        try:
            loan_examiners = LoanExaminer.objects.all()

            loan_examiner_list = []
            for loan_examiner in loan_examiners:
                loan_examiner_map = {}
                loan_examiner_map['employee_id'] = loan_examiner.employee_id_id
                loan_examiner_map['loan_examiner_id'] = loan_examiner.loan_examiner_id
                loan_examiner_map['account'] = loan_examiner.account
                loan_examiner_list.append(loan_examiner_map)

            return JsonResponse({'loan_examiner_list': loan_examiner_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=405)
    else:
        return JsonResponse({'error': "获取方式不是GET"}, status=403)


@csrf_exempt
@require_http_methods(['POST'])
def manageLoanExaminer(request):
    ''' 管理贷款审核员信息 '''

    response = {}
    with transaction.atomic():
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            operation = body.get("operation")

            if operation == "add":
                employee_id = body.get('employee_id')
                account = body.get("account")
                password = body.get("password")
                employee1 = employee.objects.get(employee_id=employee_id)


                loan_examiner = LoanExaminer(
                    employee_id=employee1,
                    account=account,
                    other_information="add a new loan examiner at " + str(datetime.datetime.now())
                )
                loan_examiner.setPassword(password)
                loan_examiner.save()

                response['response_message'] = f"成功添加一个新的贷款审查员"
                print(type(response))
            elif operation == "update":
                loan_examiner_id = body.get("loan_examiner_id")
                new_password = body.get("new_password")

                loan_examiner = LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)
                loan_examiner.setPassword(new_password)
                loan_examiner.save()

                response['response_message'] = f"成功更改贷款审查员{loan_examiner_id}的密码"
            elif operation == "delete":
                loan_examiner_id = body.get("loan_examiner_id")
                loan_examiner = LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)
                employee1 = employee.objects.get(employee_id=loan_examiner.employee_id_id)
                employee1.is_employeed = False
                loan_examiner.delete()
                employee1.save()

                response['response_message'] = f"成功删除贷款审查员{loan_examiner_id}."
            else:
                return JsonResponse({'error': "未知的操作"}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({'error': "无效的JSON 负载"}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=405)

    return JsonResponse(response)

@csrf_exempt
def getAllLoanManager(request):
    ''' 显示所有贷款部门经理的信息 '''
    if request.method == 'GET':
        try:
            loan_managers = LoanDepartmentManager.objects.all()

            loan_manager_list = []
            for loan_manager in loan_managers:
                loan_manager_map = {}
                loan_manager_map['employee_id'] = loan_manager.employee_id_id
                loan_manager_map['loan_manager_id'] = loan_manager.loan_manager_id
                loan_manager_map['account'] = loan_manager.account
                loan_manager_list.append(loan_manager_map)

            return JsonResponse({'loan_manager_list': loan_manager_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=405)
    else:
        return JsonResponse({'error': "获取方式不是GET"}, status=403)

@csrf_exempt
@require_http_methods(['POST'])
def manageLoanDepartmentManager(request):
    ''' 管理贷款部门经理信息 '''

    response = {}
    with transaction.atomic():
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            operation = body.get("operation")

            if operation == "add":
                employee_id = body.get('employee_id')
                account = body.get("account")
                password = body.get("password")
                employee1 = employee.objects.get(employee_id=employee_id)

                loan_manager = LoanDepartmentManager(
                    employee_id=employee1,
                    account=account,
                    other_information="add a new loan examiner at " + str(datetime.datetime.now())
                )
                loan_manager.setPassword(password)
                loan_manager.save()

                response['response_message'] = f"成功添加一个新贷款部门经理"
            elif operation == "update":
                loan_manager_id = body.get("loan_manager_id")
                new_password = body.get("new_password")

                loan_manager = LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)
                loan_manager.setPassword(new_password)
                loan_manager.save()

                response['response_message'] = f"成功更改贷款部门经理{loan_manager_id}的密码"
            elif operation == "delete":
                loan_manager_id = body.get("loan_manager_id")
                loan_manager = LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)
                employee1 = employee.objects.get(employee_id=loan_manager.employee_id_id)

                employee1.is_employeed = False
                loan_manager.delete()
                employee1.save()

                response['response_message'] = f"成功删除贷款部门经理{loan_manager_id}."
            else:
                return JsonResponse({'error': "不允许的操作"}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({'error': "无效的JSON 负载"}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=405)

    return JsonResponse(response)