from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Subquery, OuterRef
from foreign_exchange.models import CurrencyHolding
from foreign_exchange.models import Currency
import json

# Create your views here.
@require_http_methods(["GET"])
def get_currency_holding(request):
    response = {}

    personId = int(request.GET.get('person_id'))

    try:
        datas = []

        holdings = CurrencyHolding.objects.filter(online_user__person_id=personId)

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