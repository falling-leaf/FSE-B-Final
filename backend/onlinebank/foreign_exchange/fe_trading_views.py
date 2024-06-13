import datetime
from django.http import JsonResponse
from django.utils import timezone
from foreign_exchange.models import Currency
from django.views.decorators.csrf import csrf_exempt
from foreign_exchange.models import ForeignExchangeTrading
from django.views.decorators.http import require_http_methods
from foreign_exchange.models import account, online_user
import json

@require_http_methods(["GET"])
def currency_transfer_in(request):
    response = {}

    account_id = int(request.GET.get('account_id'))
    rmb_amount = float(request.GET.get('rmb_amount'))

    try:
        
        a = account.objects.get(account_id=account_id)
        a.transfer_in(rmb_amount)

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def currency_transfer_out(request):
    response = {}

    account_id = int(request.GET.get('account_id'))
    rmb_amount = float(request.GET.get('rmb_amount'))
    password = request.GET.get('password')

    try:
        
        a = account.objects.get(account_id=account_id)
        a.transfer_out(rmb_amount, password=password)

        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def get_user_account_name(request):
    response = {}

    user_id = int(request.GET.get('user_id'))

    try:
        
        a = online_user.objects.get(user_id=user_id)
        account_name = a.user_name

        response['name'] = account_name
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@csrf_exempt
def add_trading_history(request):
    data = json.loads(request.body)
    account_id = data.get('account_id')
    rmb_amount = data.get('rmb_amount')
    currency_amount = data.get('currency_amount')
    person_id = data.get("user_id")
    buy_or_sell = data.get("buy_or_sell")
    currency_name = data.get('currency_name')

    c = Currency.objects.get(currency_name=currency_name)

    local_time = datetime.datetime.now()

    account_ = account.objects.get(account_id=account_id)
    online_user_ = online_user.objects.get(user_id=person_id)

    sell_history = ForeignExchangeTrading(
        account=account_, 
        online_user=online_user_, 
        buy_or_sell=buy_or_sell, 
        rmb_amount=rmb_amount, 
        currency_amount=currency_amount, 
        trading_datetime=local_time,
        currency=c)
    sell_history.save()

    return JsonResponse({'status': 'success', 'message': '历史记录添加成功'})
    
@require_http_methods(["GET"])
def get_histories(request):
    response = {}

    userId = request.GET.get('userId')
    maxDatetime = request.GET.get('maxDatetime')
    minDatetime = request.GET.get('minDatetime')
    tradingState = request.GET.get('tradingState')
    currencyName = request.GET.get('currencyName')
    accountId = request.GET.get('accountId')

    try:
        datas = []

        histories = ForeignExchangeTrading.objects.all()
        if maxDatetime != None:
            histories = histories.filter(trading_datetime__lte=maxDatetime)
        if minDatetime != None:
            histories = histories.filter(trading_datetime__gte=minDatetime)
        if userId != None:
            histories = histories.filter(online_user__user_id=userId)
        if tradingState != None:
            histories = histories.filter(buy_or_sell=(tradingState == '买入'))
        if currencyName != None:
            histories = histories.filter(currency__currency_name=currencyName)
        if accountId != None:
            histories = histories.filter(account__account_id=accountId)

        for h in histories:
            trading_state = 'Default'
            if h.buy_or_sell == True:
                trading_state = '买入'
            else:
                trading_state = '卖出'
            datas.append({
                'account_id': h.account.account_id,
                'currency_id': h.currency.currency_id,
                'currency_name': h.currency.currency_name,
                'trading_state': trading_state,
                'rmb_amount': h.rmb_amount,
                'currency_amount': h.currency_amount,
                'trading_datetime': h.trading_datetime,
            })

        response['histories'] = datas
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
