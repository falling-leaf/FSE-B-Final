from django.shortcuts import render
import json
from django.views.decorators.http import require_http_methods
from common.models import employee
from foreign_exchange.models import ForeignExchangeOperator
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

@require_http_methods(["GET"])
def handlesearchallOperator(request):
    curPage = int(request.GET.get('nowPage')) - 1
    operators = ForeignExchangeOperator.objects.all()
    results = []
    for operator in operators:
        employee_name = operator.employee.employee_name
        add_authority = operator.add_authority
        delete_authority = operator.delete_authority
        alter_name_authority = operator.alter_name_authority
        alter_rate_authority = operator.alter_rate_authority
        account = operator.account
        result = {
            'employee_id': operator.employee.employee_id,
            'foreign_exchange_operator_id': operator.foreign_exchange_operator_id,
            'employee_name': employee_name,
            'account': account,
            'add_authority': add_authority,
            'delete_authority': delete_authority,
            'alter_name_authority': alter_name_authority,
            'alter_rate_authority': alter_rate_authority
        }
        results.append(result)

    paginator = Paginator(results, 11)  # 每页11条记录
    page_results = paginator.get_page(curPage + 1)  # 获取指定页的记录

    serialized_results = []
    for result in page_results:
        serialized_results.append(result)

    return JsonResponse({'results': serialized_results})

@require_http_methods(["GET"])
def handleSearch(request):
    search_name = request.GET.get('name')
    curPage = int(request.GET.get('nowPage')) - 1
    operators = ForeignExchangeOperator.objects.filter(employee__employee_name__icontains = search_name)
    results = []
    for operator in operators:
        employee_name = operator.employee.employee_name
        add_authority = operator.add_authority
        delete_authority = operator.delete_authority
        alter_name_authority = operator.alter_name_authority
        alter_rate_authority = operator.alter_rate_authority
        account = operator.account
        result = {
            'employee_id': operator.employee.employee_id,
            'foreign_exchange_operator_id': operator.foreign_exchange_operator_id,
            'employee_name': employee_name,
            'account': account,
            'add_authority': add_authority,
            'delete_authority': delete_authority,
            'alter_name_authority': alter_name_authority,
            'alter_rate_authority': alter_rate_authority
        }
        results.append(result)

    paginator = Paginator(results, 11)  # 每页11条记录
    page_results = paginator.get_page(curPage + 1)  # 获取指定页的记录

    serialized_results = []
    for result in page_results:
        serialized_results.append(result)

    return JsonResponse({'results': serialized_results})


@csrf_exempt
def handleDeleteOperator(request):
    data = json.loads(request.body)
    employee_id_to_delete = data.get('employee_id')
    operator_id = data.get('foreign_exchange_operator_id')
    try:
        operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
        employees = employee.objects.get(employee_id = employee_id_to_delete)
        employees.is_employeed = False
        operator.delete()
        employees.save()
        return JsonResponse({'status': 'success', 'message': '操作员删除成功'})
    except ForeignExchangeOperator.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '未找到操作员' })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt
def handleModifyOperator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            checked_values = data.get('checkedValues')
            operator_id = data.get('foreign_exchange_operator_id')
            a = 0
            b = 0
            c = 0
            d = 0
            operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
            for check_value in checked_values:
                if(check_value =='1'):
                    operator.add_authority = True
                    a=1
                if(check_value =='2'):
                    operator.delete_authority = True
                    b=1
                if(check_value == '3'):
                    operator.alter_rate_authority = True
                    c=1
                if(check_value == '4'):
                    operator.alter_name_authority = True
                    d=1
            if(a==0):
                operator.add_authority = False
            if(b==0):
                operator.delete_authority = False
            if(c==0):
                operator.alter_rate_authority = False
            if(d==0):
                operator.alter_name_authority = False


            try:
                operator.save()
                response_data = {
                'status': 'success',
                'message': '修改 Currency 成功'
            }
            except Exception as e:
                response_data = {
                    'status': 'error',
                    'message': str(e)
                }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    
@csrf_exempt
def handleAddOperator(request):
    
    data = json.loads(request.body)
    employee_name = data.get('employee_name')
    identity_card = data.get('identity_card')
    phone_number = data.get('phone_number')
    password = data.get('password')
    other_information = data.get('other_information')
    checked_values = data.get('checkedValues')
    selectedOption = data.get('selectedOption')
    account = data.get('account')

    a = 0
    b = 0
    c = 0
    d = 0
    for check_value in checked_values:
        if(check_value =='1'):
            add_authority = True
            a=1
        if(check_value =='2'):
            delete_authority = True
            b=1
        if(check_value == '3'):
            alter_rate_authority = True
            c=1
        if(check_value == '4'):
            alter_name_authority = True
            d=1
    if(a==0):
        add_authority = False
    if(b==0):
        delete_authority = False
    if(c==0):
        alter_rate_authority = False
    if(d==0):
        alter_name_authority = False

    if(selectedOption == 'female'):
        employee_sex = 0
    if(selectedOption == 'male'):
        employee_sex = 1

    new_employee = employee(
        employee_name = employee_name,
        identity_card = identity_card,
        employee_sex = employee_sex,
        phone_number = phone_number,
        occupation_name = '外汇操作员',
        is_employeed = True,
        other_information = other_information
    )
    try:
        new_employee.save()
    except Exception as e:
        response_data = {
            'status': 'error',
            'message': '插入 Employee 失败',
            'error': str(e)
        }
        
    
    new_operator = ForeignExchangeOperator(
        employee = new_employee,
        account = account,
        password = password,
        add_authority = add_authority,
        delete_authority = delete_authority,
        alter_name_authority = alter_name_authority,
        alter_rate_authority = alter_rate_authority
    )
    try:
        new_operator.save()
        response_data = {
                'status': 'success',
                'message': '添加成功'
            }
    except Exception as e:
            response_data = {
                'status': 'error',
                'message': str(e)
            }
    return JsonResponse(response_data)