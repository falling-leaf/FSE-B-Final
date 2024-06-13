from django.shortcuts import render
from foreign_exchange.models import RateUpdateRecord
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from foreign_exchange.models import Currency
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max, Subquery, OuterRef
from datetime import timedelta
from django.core.paginator import Paginator
import json
from django.db.models import Count
from django.db.models.functions import TruncDate
# Create your views here.
@require_http_methods(["GET"])
def show_rate_update_record(request):
    response = {}

    curPage = int(request.GET.get('curPage')) - 1
    maxDate = request.GET.get('maxDateCondition')
    minDate = request.GET.get('minDateCondition')
    category = request.GET.get('categoryCondition')

    try:
        records = RateUpdateRecord.objects.all()
        
        if category != None:
            records = records.filter(
                currency__currency_name=category
            )
            if maxDate != None:
                records = records.filter(
                    update_datetime__lte=maxDate
                )
            if minDate != None:
                records = records.filter(
                    update_datetime__gte=minDate
                )
            records = records.order_by('-update_datetime')[curPage * 11:curPage * 11 + 11]
        else:
            subquery = RateUpdateRecord.objects.filter(
                currency__currency_name=OuterRef('currency__currency_name')
            ).values(
                'currency__currency_name'
            ).annotate(
                max_update_datetime=Max('update_datetime')
            ).values(
                'max_update_datetime'
            )
            records = RateUpdateRecord.objects.filter(
                update_datetime__in=Subquery(subquery)
            ).order_by(
                'currency__currency_name'
            )[curPage * 11:curPage * 11 + 11]
        
        names = []
        for record in records:
            currency_name = Currency.GetCurrencyName(currencyId=record.currency.currency_id)
            names.append(currency_name)

        record = serializers.serialize("json", records, cls=DjangoJSONEncoder)
        response['record'] = json.loads(record)
        name = serializers.serialize("json", names, cls=DjangoJSONEncoder)
        response['name'] = json.loads(name)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

def initial_trend(series, season_len):
    total = 0.0
    for i in range(season_len):
        total += (series[i + season_len] - series[i]) / season_len
    return total / season_len

def initial_seasonal_components(series, season_len):
    seasonals = {}
    season_averages = []
    n_seasons = len(series) // season_len

    for j in range(n_seasons):
        season_averages.append(sum(series[season_len * j:season_len * j + season_len]) / season_len)

    for i in range(season_len):
        total = 0.0
        for j in range(n_seasons):
            total += series[season_len * j + i] - season_averages[j]
        seasonals[i] = total / n_seasons

    return seasonals

def holt_winters_additive(series, season_len, alpha, beta, gamma, n_preds):
    result = []
    seasonals = initial_seasonal_components(series, season_len)
    #print(seasonals)
    for i in range(len(series) + n_preds):
        #print(i)
        if i == 0:
            smooth = series[0]
            trend = initial_trend(series, season_len)
            result.append(series[0])
            continue
        if i >= len(series):
            m = i - len(series) + 1
            result.append((smooth + m * trend) + seasonals[i % season_len])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha * (val - seasonals[i % season_len]) + (1 - alpha) * (smooth + trend)
            trend = beta * (smooth - last_smooth) + (1 - beta) * trend
            seasonals[i % season_len] = gamma * (val - smooth) + (1 - gamma) * seasonals[i % season_len]
            result.append(smooth + trend + seasonals[i % season_len])
    return result

@require_http_methods(["GET"])
def get_simulation_data(request):

    response = {}

    currency_id = int(request.GET.get('currency_id'))

    try:
        latest_30_days = RateUpdateRecord.objects.filter(currency__currency_id=currency_id).values('update_datetime').annotate(
            date=TruncDate('update_datetime')
        ).values('date').annotate(max_update_datetime=Max('update_datetime')).order_by('-max_update_datetime')[:30]

        data = RateUpdateRecord.objects.filter(currency__currency_id=currency_id, update_datetime__in=[item['max_update_datetime'] for item in latest_30_days])

        data = data.order_by('-update_datetime')
        simulation_data = []
        buying_rate = []
        selling_rate = []
        for d in data:
            simulation_data.insert(0, {
                'buying_rate': d.buying_rate,
                'selling_rate': d.selling_rate,
                'update_datetime': d.update_datetime
            })
            buying_rate.insert(0, float(d.buying_rate))
            selling_rate.insert(0, float(d.selling_rate))
        num = len(data)
        if num == 1:
            response['msg'] = '数据量过少'
            response['error_num'] = 2
            return JsonResponse(response)
        last_date = simulation_data[num - 1]['update_datetime']
    
        season_len = min(7, num//2)
        alpha = 0.2
        beta = 0.2
        gamma = 0.2
        n_preds = min(7, num//2)

        buying_rate = holt_winters_additive(buying_rate, season_len, alpha, beta, gamma, n_preds)
        #print(buying_rate)
        selling_rate = holt_winters_additive(selling_rate, season_len, alpha, beta, gamma, n_preds)
        #print(selling_rate)
        for i in range(1, min(7, num//2) + 1):
            new_date = last_date + timedelta(days=i)
            new_simulation_data = {
                'buying_rate': buying_rate[num - 1 + i],
                'selling_rate': selling_rate[num - 1 + i],
                'update_datetime': new_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            simulation_data.append(new_simulation_data)

        response['simulation_data'] = simulation_data
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
    

@require_http_methods(["GET"])
def handleshow(request):
    response = {}
    curPage = int(request.GET.get('curPage')) - 1
    try:
        records = RateUpdateRecord.objects.all()       
        subquery = RateUpdateRecord.objects.filter(
            currency__currency_name=OuterRef('currency__currency_name')
        ).values(
            'currency__currency_name'
        ).annotate(
            max_update_datetime=Max('update_datetime')
        ).values(
            'max_update_datetime'
        )
        records = RateUpdateRecord.objects.filter(
            update_datetime__in=Subquery(subquery)
        ).order_by(
            'currency__currency_name'
        )[curPage * 11:curPage * 11 + 11]
        
        names = []
        for record in records:
            currency_name = Currency.GetCurrencyName(currencyId=record.currency.currency_id)
            names.append(currency_name)

        record = serializers.serialize("json", records, cls=DjangoJSONEncoder)
        response['record'] = json.loads(record)
        name = serializers.serialize("json", names, cls=DjangoJSONEncoder)
        response['name'] = json.loads(name)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def handlesearch(request):
    search_name = request.GET.get('name')
    curPage = int(request.GET.get('curPage')) - 1
    currency_records = RateUpdateRecord.objects.filter(currency__currency_name__icontains = search_name)
    latest_updates = {}
    for record in currency_records:
        currency_name = record.currency.currency_name
        update_time = record.update_datetime

        if currency_name in latest_updates:
            if update_time > latest_updates[currency_name]:
                latest_updates[currency_name] = update_time
        else:
            latest_updates[currency_name] = update_time

    results = []
    for currency_name, latest_update_time in latest_updates.items():
        latest_record = currency_records.filter(currency__currency_name=currency_name, update_datetime=latest_update_time).first()
        result = {
            'currency_name': latest_record.currency.currency_name,
            'buying_rate': latest_record.buying_rate,
            'selling_rate': latest_record.selling_rate,
            'update_datetime': latest_record.update_datetime.strftime('%Y-%m-%d %H:%M:%S')
        }
        results.append(result)

    
    paginator = Paginator(results, 11)  # 每页11条记录
    page_results = paginator.get_page(curPage + 1)  # 获取指定页的记录

    serialized_results = []
    for result in page_results:
        serialized_results.append(result)

    return JsonResponse({'results': serialized_results})
    