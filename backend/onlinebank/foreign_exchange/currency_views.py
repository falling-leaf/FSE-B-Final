from django.shortcuts import render
from foreign_exchange.models import Currency
from foreign_exchange.models import RateUpdateRecord
from foreign_exchange.models import account
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from foreign_exchange.models import ForeignExchangeOperator
from django.core import serializers
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import calendar
import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
import json
# Create your views here.
def get_all_currency(request):
    response = {}

    try:
        currencies = Currency.objects.all()
        data = [{'label': currency.currency_name, 'value': currency.currency_name} for currency in currencies]
        data.append({'label': '(空)', 'value': ''})
        # print(data)
        response['data'] = data
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

def get_currency(request):
    response = {}

    currencyName = request.GET.get('currency_name')

    try:
        currencies = Currency.objects.filter(currency_name=currencyName)
        data = []

        for c in currencies:
            data.append({
                'buying_rate': c.latest_exchange_buying_rate,
                'selling_rate': c.latest_exchange_selling_rate,
            })

        # print(data)
        response['rates'] = data
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@csrf_exempt
def handleDeleteCurrency(request):
    data = json.loads(request.body)
    currency_id_to_delete = data.get('currency_id')
    operator_id = data.get('operator_id')
    operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
    if(operator.delete_authority == False):
        return JsonResponse({'status': 'error', 'message': '无删除外币的权限！' })
    else:
        try:
            currency = Currency.objects.get(currency_id = currency_id_to_delete)
            currency.delete()
            return JsonResponse({'status': 'success', 'message': 'Currency deleted successfully'})
        except Currency.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Currency not found' })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
@csrf_exempt
def handleAddCurrency(request):
    
    data = json.loads(request.body)
    currency_name = data.get('currency_name')
    currency_latest_buy_rate = data.get('latest_exchange_buying_rate')
    currency_latest_sell_rate = data.get('latest_exchange_selling_rate')
    operator_id = data.get('operator_id')
    
    operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
    if(operator.add_authority == False):
        return JsonResponse({'status': 'error', 'message': '无新增外币的权限！' })
    else:
        try:
            new_currency = Currency(
                currency_name = currency_name,
                latest_exchange_buying_rate = currency_latest_buy_rate,
                latest_exchange_selling_rate = currency_latest_sell_rate
                )
            new_currency.save()
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': str(e),
            }
            return JsonResponse(response_data)
        current_time = datetime.datetime.now()
        try:
            new_update_record = RateUpdateRecord(
                currency = new_currency,
                buying_rate = currency_latest_buy_rate,
                selling_rate= currency_latest_sell_rate,
                update_datetime = current_time
            )
            new_update_record.save()
            return JsonResponse({'status': 'success', 'message': 'Currency added successfully'})
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': str(e)
            }
            return JsonResponse(response_data)

@csrf_exempt
def handleModifyRateCurrency(request):
    
    data = json.loads(request.body)
    currency_id = data.get('currency_id')
    modify_buy_rate = data.get('buying_rate')
    modify_sell_rate = data.get('selling_rate')
    operator_id = data.get('operator_id')
    operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
    if(operator.alter_rate_authority == False):
        return JsonResponse({'status': 'error', 'message': '无修改汇率的权限！' })
    else:
        try:
            currency = Currency.objects.get(currency_id = currency_id)
            currency.latest_exchange_buying_rate = modify_buy_rate
            currency.latest_exchange_selling_rate = modify_sell_rate
            currency.save()
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': '修改 Currency 失败',
                'error': str(e)
            }
        
        current_time = datetime.datetime.now()
        try:
            new_update_record = RateUpdateRecord(
                currency = currency,
                buying_rate = modify_buy_rate,
                selling_rate= modify_sell_rate,
                update_datetime = current_time
            )
            new_update_record.save()
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
    

@csrf_exempt
def handleModifyNameCurrency(request):
    
    data = json.loads(request.body)
    currency_id = data.get('currency_id')
    modify_name = data.get('currency_name')
    operator_id = data.get('operator_id')
    operator = ForeignExchangeOperator.objects.get(foreign_exchange_operator_id = operator_id)
    if(operator.alter_name_authority == False):
        return JsonResponse({'status': 'error', 'message': '无重命名的权限！' })
    else:
        try:
            currency = Currency.objects.get(currency_id = currency_id)
            currency.currency_name = modify_name
            currency.save()
            response_data = {
                'status': 'success',
                'message': '重命名 Currency 成功'
            }
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': '重命名 Currency 失败',
                'error': str(e)
            }           
    return JsonResponse(response_data)

@csrf_exempt
def login(request):
    
    data = json.loads(request.body)
    account_id = data.get('account_id')
    password = data.get('password')

    account_ = account.objects.get(account_id=account_id)
    password_ = account_.password
    if(password != password_):
        return JsonResponse({'status': 'error', 'message': '密码错误！' })
    else:
        try:
            response_data = {
                'status': 'success',
                'message': '密码正确！'
            }
        except Exception as e:
            response_data = {
                'status': 'error',
                'message': '不知道为什么错了',
                'error': str(e)
            }           
    return JsonResponse(response_data)