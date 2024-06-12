from django.http import JsonResponse
from django.utils import timezone
from foreign_exchange.models import Currency
from django.views.decorators.csrf import csrf_exempt
from foreign_exchange.models import ForeignExchangeTrading
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt  # 可选：用于处理跨站请求伪造（CSRF）保护
def createTradeData(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # 从POST请求的body中获取参数
        account_id = data.get('account_id')
        rmb_amount = data.get('rmb_amount')
        currency_amount = data.get('currency_amount')
        person_id = data.get("person_id")
        buy_or_sell = data.get("buy_or_sell")
        currency_id = data.get('currency_id')
        # 获取当前UTC时间
        current_utc_time = timezone.now()

        # 转换为本地时间
        local_time = current_utc_time.astimezone(timezone.get_current_timezone())

        # 提取日期和时间部分
        date_part = local_time.date()
        time_part = local_time.time()
        sell_history = ForeignExchangeTrading(account__account_id=account_id, online_user__user_id = person_id, buy_or_sell = buy_or_sell, rmb_amount=rmb_amount, currency_amount=currency_amount, trading_datetime= date_part, trading_time = time_part,currency__currency_id = currency_id)
        sell_history.save()
        # 在这里进行进一步的处理和逻辑操作

        return JsonResponse({'message': 'Sell request processed successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
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
            histories = histories.filter(online_user__person_id=userId)
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
