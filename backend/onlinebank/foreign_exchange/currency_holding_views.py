from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Subquery, OuterRef
from foreign_exchange.models import CurrencyHolding
from foreign_exchange.models import Currency
from foreign_exchange.models import account
import json

# Create your views here.
@require_http_methods(["GET"])
def get_currency_holding(request):
    response = {}

    personId = int(request.GET.get('person_id'))

    try:
        datas = []

        holdings = CurrencyHolding.objects.filter(online_user__user_id=personId)

        for h in holdings:
            datas.append({
                'currency_id': h.currency.currency_id,
                'currency_name': h.currency.currency_name,
                'amount': h.amount
            })

        response['holdings'] = datas
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def confirm_currency_holding(request):
    response = {}

    personId = int(request.GET.get('person_id'))
    currencyName = request.GET.get('currency_name')

    try:
        datas = []

        holdings = CurrencyHolding.objects.filter(online_user__user_id=personId)

        holdings = holdings.filter(currency__currency_name=currencyName)

        for h in holdings:
            datas.append({
                'currency_id': h.currency.currency_id,
                'currency_name': h.currency.currency_name,
                'amount': h.amount
            })

        response['holdings'] = datas
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def get_accounts(request):
    response = {}

    personId = int(request.GET.get('user_id'))

    try:
        accounts = account.objects.filter(user_id__user_id=request.GET.get('user_id'))
        #print(accounts)
        datas = [{'label': a.account_id, 'value': a.account_id} for a in accounts]
        print(datas)
        response['data'] = datas
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
        print(e)

    return JsonResponse(response)

@require_http_methods(["GET"])
def update_holding(request):
    response = {}

    user_id = int(request.GET.get('user_id'))
    currency_name = request.GET.get('currency_name')
    currency_amount = float(request.GET.get('currency_amount'))

    try:

        holdings = CurrencyHolding.objects.filter(online_user__user_id=user_id)
        holding = holdings.get(currency__currency_name=currency_name)
        holding.amount = currency_amount
        holding.save()

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)