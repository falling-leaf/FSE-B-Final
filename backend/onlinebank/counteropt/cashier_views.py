import json
import datetime

import pytz
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@csrf_exempt
def cashier_add(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashierID'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无开设账户权限"}, status=403)
        filter_account = account.objects.filter(identity_card=data.get('identity_card'))
        if filter_account.count() >= 4:
            return JsonResponse({"error": "账户数量超过限制"}, status=403)
        check_idcard = data.get('identity_card')
        check_user = online_user.objects.filter(identity_card = check_idcard)
        if check_user.exists():
            new_account = account(
            password=data.get('password'),
            identity_card=data.get('identity_card'),
            card_type=1,#1为银行卡
            phone_num = check_user[0].phone_num,
            user_id = check_user[0]
            )
        else: 
            print(data)
            new_account = account(
                password=data.get('password'),
                identity_card=data.get('identity_card'),
                phone_num = data.get('phone_num'),
                card_type=1,#1为银行卡
            )
        new_account.save()
        return_data = {'id': new_account.account_id, "success": "开设账户成功"}
        return JsonResponse(return_data, status=200)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def cashier_query_account(request):
    if request.method == 'GET':
        filter_accountss = account.objects.filter(account_id=request.GET.get('accountID'))
        if not filter_accountss.exists():
            return JsonResponse({"error": "不存在该账户"}, status=403)
        filter_accounts = filter_accountss[0]
        account_data = {}
        account_data['id'] = filter_accounts.account_id
        account_data['password'] = filter_accounts.password
        account_data['identity_card'] = filter_accounts.identity_card
        account_data['balance'] = filter_accounts.balance
        account_data['currentDeposit'] = filter_accounts.current_deposit
        account_data['uncreditedDeposit'] = filter_accounts.uncredited_deposit
        account_data['isFrozen'] = filter_accounts.is_frozen
        account_data['isLost'] = filter_accounts.is_lost
        return JsonResponse(account_data, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_deposit_record_list(dic):
    deposits = deposit_record.objects.filter(**dic)
    deposit_record_list = list()
    for deposit in deposits:
        deposit_return = {}
        deposit_return['deposit_record_id'] = deposit.deposit_record_id
        deposit_return['account_id'] = deposit.account_id
        deposit_return['deposit_type'] = deposit.deposit_type
        deposit_return['auto_renew_status'] = deposit.auto_renew_status
        deposit_return['deposit_start_date'] = deposit.deposit_start_date
        deposit_return['deposit_end_date'] = deposit.deposit_end_date
        deposit_return['deposit_amount'] = deposit.deposit_amount
        deposit_return['cashier_id'] = deposit.cashier_id
        deposit_record_list.append(deposit_return)
    return deposit_record_list


# 查询所有的存款记录
def cashier_all_deposits(request):
    if request.method == 'GET':
        dic = {}
        deposit_record_list = get_deposit_record_list(dic)
        return JsonResponse(deposit_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 活期存款
@csrf_exempt
def cashier_demand_deposit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashier_id'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].trade_authority:
            return JsonResponse({"error": "柜员无交易操作权限"}, status=403)
        if data.get('deposit_amount') <= 0:
            return JsonResponse({"error": "活期存款金额错误"}, status=403)
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            filter_account = filter_account.first()
            check_idcard = filter_account.identity_card
            check_user = online_user.objects.filter(identity_card = check_idcard)
            if check_user.exists():
                if check_user[0].is_blacklisted:
                    return JsonResponse({"error": "账户已被列入黑名单，无法执行任何操作"}, status=403)
            if filter_account.is_frozen or filter_account.is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 更新用户存款情况
            filter_account.uncredited_deposit += data.get('deposit_amount')
            filter_account.balance += data.get('deposit_amount')
            filter_account.save()
            # 更新存款记录
            new_deposit_record = deposit_record(
                account_id=data.get('account_id'),
                deposit_type='活期存款',
                deposit_start_date=datetime.datetime.now(),
                deposit_update_date=datetime.datetime.now(),
                deposit_amount=data.get('deposit_amount'),
                cashier_id=data.get('cashier_id'),
            )
            new_deposit_record.save()
            return JsonResponse({"success": "存款成功"}, status=200)
        else:
            check_account = account.objects.filter(account_id=data.get('account_id'))
            if not check_account.exists():
                return JsonResponse({"error": "账户不存在"}, status=403)
            else: return JsonResponse({"error": "密码错误"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 定期存款
@csrf_exempt
def cashier_time_deposit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashier_id'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].trade_authority:
            return JsonResponse({"error": "柜员无交易操作权限"}, status=403)
        if data.get('deposit_amount') <= 0:
            return JsonResponse({"error": "定期存款金额错误"}, status=403)
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            filter_account = filter_account.first()
            check_idcard = filter_account.identity_card
            check_user = online_user.objects.filter(identity_card = check_idcard)
            if check_user.exists():
                if check_user[0].is_blacklisted:
                    return JsonResponse({"error": "账户已被列入黑名单，无法执行任何操作"}, status=403)
            if filter_account.is_frozen or filter_account.is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 更新用户存款情况
            filter_account.current_deposit += data.get('deposit_amount')
            #filter_account.balance += data.get('deposit_amount')
            filter_account.save()
            check_deposit_term = data.get('deposit_term')
            if "." in check_deposit_term:
                check_deposit_term = int(float(check_deposit_term))
            else: check_deposit_term = int(check_deposit_term)
            # 更新存款记录
            new_deposit_record = deposit_record(
                account_id=data.get('account_id'),
                deposit_type='定期存款',
                auto_renew_status=data.get('auto_renew_status'),
                deposit_start_date=datetime.datetime.now(),
                deposit_update_date=datetime.datetime.now(),
                deposit_end_date=datetime.datetime.now() + datetime.timedelta(days=check_deposit_term * 30),
                deposit_amount=data.get('deposit_amount'),
                cashier_id=data.get('cashier_id'),
            )
            new_deposit_record.save()
            return JsonResponse({"success": "存款成功"}, status=200)
        else:
            check_account = account.objects.filter(account_id=data.get('account_id'))
            if not check_account.exists():
                return JsonResponse({"error": "账户不存在"}, status=403)
            else: return JsonResponse({"error": "密码错误"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 累计存款
def cashier_total_deposit(request):
    if request.method == 'GET':
        filter_account = account.objects.filter(account_id=request.GET.get('account_id'),
                                                password=request.GET.get('password'))
        if filter_account.exists():
            total_deposit = {}
            total_deposit['total_amount'] = filter_account[0].balance
            return JsonResponse(total_deposit, safe=False)
        else:
            return JsonResponse({"error": "User not exists"}, status=403)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_with_drawls_record_list(dic):
    with_drawls = withdrawal_record.objects.filter(**dic)
    with_drawls_record_list = list()
    for with_drawl in with_drawls:
        with_drawls_return = {}
        with_drawls_return['withdrawl_record_id'] = with_drawl.withdrawal_record_id
        with_drawls_return['account_id'] = with_drawl.account_id
        with_drawls_return['withdrawl_date'] = with_drawl.withdrawal_date
        with_drawls_return['withdrawl_amount'] = with_drawl.withdrawal_amount
        with_drawls_return['cashier_id'] = with_drawl.cashier_id
        with_drawls_record_list.append(with_drawls_return)
    return with_drawls_record_list


# 查询所有取款记录
def cashier_all_withdrawls(request):
    if request.method == 'GET':
        dic = {}
        with_drawls_record_list = get_with_drawls_record_list(dic)
        return JsonResponse(with_drawls_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 取款
@csrf_exempt
def cashier_withdrawl(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashier_id'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].trade_authority:
            return JsonResponse({"error": "柜员无交易操作权限"}, status=403)
        if data.get('withdrawl_amount') <= 0:
            return JsonResponse({"error": "取款金额错误"}, status=403)
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            filter_account = filter_account.first()
            check_idcard = filter_account.identity_card
            check_user = online_user.objects.filter(identity_card = check_idcard)
            if check_user.exists():
                if check_user[0].is_blacklisted:
                    return JsonResponse({"error": "账户已被列入黑名单，无法执行任何操作"}, status=403)
            if filter_account.is_frozen or filter_account.is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 判断用户存款是否满足取出条件
            if filter_account.uncredited_deposit >= data.get('withdrawl_amount'):
                # 更新用户存款情况
                filter_account.uncredited_deposit -= data.get('withdrawl_amount')
                filter_account.balance -= data.get('withdrawl_amount')
                filter_account.save()
                # 更新取款记录
                new_withdrawal_record = withdrawal_record(
                    account_id=data.get('account_id'),
                    # --此处存疑--
                    withdrawal_date=datetime.datetime.now(),
                    # -----
                    withdrawal_amount=data.get('withdrawl_amount'),
                    cashier_id=data.get('cashier_id'),
                )
                new_withdrawal_record.save()
                return JsonResponse({"success": "取款成功"}, status=200)
            else:
                return JsonResponse({"error": "存款不足"}, status=403)
        else:
            check_account = account.objects.filter(account_id=data.get('account_id'))
            if not check_account.exists():
                return JsonResponse({"error": "账户不存在"}, status=403)
            else: return JsonResponse({"error": "密码错误"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_transfer_record_list(dic):
    transfers = transfer_record.objects.filter(**dic)
    transfer_record_list = list()
    for transfer in transfers:
        transfers_return = {}
        transfers_return['transfer_record_id'] = transfer.transfer_record_id
        transfers_return['account_in_id'] = transfer.account_in_id
        transfers_return['account_out_id'] = transfer.account_out_id
        transfers_return['transfer_date'] = transfer.transfer_date
        transfers_return['transfer_amount'] = transfer.transfer_amount
        transfers_return['cashier_id'] = transfer.cashier_id
        transfer_record_list.append(transfers_return)
    return transfer_record_list


# 转账记录查询
def cashier_all_transfers(request):
    if request.method == 'GET':
        dic = {}
        transfer_record_list = get_transfer_record_list(dic)
        return JsonResponse(transfer_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 转账
@csrf_exempt
def cashier_transfer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashier_id'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].trade_authority:
            return JsonResponse({"error": "柜员无交易操作权限"}, status=403)
        if data.get('transfer_amount') <= 0:
            return JsonResponse({"error": "转账金额错误"}, status=403)
        filter_out_account = account.objects.filter(account_id=data.get('account_out_id'), password=data.get('password'))
        filter_in_account = account.objects.filter(account_id=data.get('account_in_id'))
        if not filter_in_account.exists():
            return JsonResponse({"error": "接收转账用户不存在"}, status=403)
        if not filter_out_account.exists():
            check_account = account.objects.filter(account_id=data.get('account_id'))
            if not check_account.exists():
                return JsonResponse({"error": "账户不存在"}, status=403)
            else: return JsonResponse({"error": "密码错误"}, status=403)
        filter_in_account = filter_in_account.first()
        filter_out_account = filter_out_account.first()
        check_idcard = filter_in_account.identity_card
        check_user = online_user.objects.filter(identity_card = check_idcard)
        if check_user.exists():
            if check_user[0].is_blacklisted:
                return JsonResponse({"error": "转入账户已被列入黑名单，无法执行任何操作"}, status=403)
        check_idcard = filter_out_account.identity_card
        check_user = online_user.objects.filter(identity_card = check_idcard)
        if check_user.exists():
            if check_user[0].is_blacklisted:
                return JsonResponse({"error": "转出账户已被列入黑名单，无法执行任何操作"}, status=403)
        if filter_out_account.is_frozen or filter_out_account.is_lost:
            return JsonResponse({"error": "转出账户挂失/冻结"}, status=403)
        if filter_in_account.is_frozen or filter_in_account.is_lost:
            return JsonResponse({"error": "转入账户挂失/冻结"}, status=403)
        # 判断用户存款是否满足取出条件
        if filter_out_account.uncredited_deposit >= data.get('transfer_amount'):
            # 更新用户存款情况
            filter_out_account.uncredited_deposit -= data.get('transfer_amount')
            filter_out_account.balance -= data.get('transfer_amount')
            filter_out_account.save()
            filter_in_account.uncredited_deposit += data.get('transfer_amount')
            filter_in_account.balance += data.get('transfer_amount')
            filter_in_account.save()
            # 更新取款记录
            new_transfer_record = transfer_record(
                account_in_id=data.get('account_in_id'),
                account_out_id=data.get('account_out_id'),
                # --此处存疑--
                transfer_date=datetime.datetime.now(),
                # -----
                transfer_amount=data.get('transfer_amount'),
                cashier_id=data.get('cashier_id'),
            )
            new_transfer_record.save()
            return JsonResponse({"success": "successful operation"}, status=200)
        else:
            return JsonResponse({"error": "存款不足"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 查询所有交易记录
def cashier_all_records(request):
    if request.method == 'GET':
        if (request.GET.get('account_id') != ''
                and not account.objects.filter(account_id=int(request.GET.get('account_id'))).exists()):
            # print("Invalid account_id")
            return JsonResponse({"error": "查询的用户不存在"}, status=403)
        if request.GET.get('type') == '1':
            dic = {}
            dic['account_id'] = int(request.GET.get('account_id'))
            deposit_record_list = get_deposit_record_list(dic)
            return JsonResponse(deposit_record_list, safe=False)
        elif request.GET.get('type') == '2':
            dic = {}
            dic['account_id'] = int(request.GET.get('account_id'))
            with_drawls_record_list = get_with_drawls_record_list(dic)
            return JsonResponse(with_drawls_record_list, safe=False)
        elif request.GET.get('type') == '3':
            dic_in = {}
            dic_out = {}
            dic_in['account_in_id'] = int(request.GET.get('account_id'))
            dic_out['account_out_id'] = int(request.GET.get('account_id'))
            transfer_record_list_in = get_transfer_record_list(dic_in)
            transfer_record_list_out = get_transfer_record_list(dic_out)
            transfer_record_list = transfer_record_list_in + transfer_record_list_out
            # print(transfer_record_list)
            return JsonResponse(transfer_record_list, safe=False)
        return JsonResponse({"error": "传入参数错误"}, status=403)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 改变自动续期状态
@csrf_exempt
def cashier_update_auto_renew(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashier_id'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无交易操作权限"}, status=403)
        modify_deposit = deposit_record.objects.get(deposit_record_id=data.get("record_id"))
        if (account.objects.get(account_id=modify_deposit.account_id).is_frozen
                or account.objects.get(account_id=modify_deposit.account_id).is_lost):
            return JsonResponse({"error": "账户冻结/挂失"}, status=403)
        modify_deposit.auto_renew_status = not modify_deposit.auto_renew_status
        modify_deposit.save()
        return JsonResponse({"success": "successful operation"}, status=200)
    elif request.method == "OPTIONS":
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 后端启动时自动更新定期存款金额
def time_deposit_record_update():
    print("开始更新定期存款金额")
    deposits = deposit_record.objects.all()
    time_deposit_rate = 0.0003
    today = datetime.date.today()
    # today = today + datetime.timedelta(days=450)
    for deposit in deposits:
        filter_account = account.objects.get(account_id=deposit.account_id)
        # 定期存款
        if deposit.deposit_type == '定期存款':
            # 没有添加自动续期且超时
            if (today > deposit.deposit_end_date > deposit.deposit_update_date
                    and not deposit.auto_renew_status):
                delta_time = deposit.deposit_end_date - deposit.deposit_update_date
                month = int(delta_time.days/30)
                org_current_deposit = filter_account.current_deposit
                for i in range(month):
                    filter_account.current_deposit += filter_account.uncredited_deposit * time_deposit_rate
                filter_account.balance += filter_account.current_deposit - org_current_deposit
                deposit.deposit_update_date = deposit.deposit_update_date + datetime.timedelta(days=month*30)
                filter_account.save()
                deposit.save()
                continue
            # 添加了自动续期且超时
            if (today > deposit.deposit_end_date > deposit.deposit_update_date
                    and deposit.auto_renew_status):
                delta_time = today - deposit.deposit_update_date
                month = int(delta_time.days / 30)
                org_current_deposit = filter_account.current_deposit
                for i in range(month):
                    filter_account.current_deposit += filter_account.uncredited_deposit * time_deposit_rate
                filter_account.balance += filter_account.current_deposit - org_current_deposit
                deposit.deposit_update_date = deposit.deposit_update_date + datetime.timedelta(days=month * 30)
                while deposit.deposit_end_date <= deposit.deposit_update_date:
                    deposit.deposit_end_date += deposit.deposit_end_date - deposit.deposit_start_date
                filter_account.save()
                deposit.save()
                continue
            # 未超时
            delta_time = today - deposit.deposit_update_date
            month = int(delta_time.days / 30)
            org_current_deposit = filter_account.current_deposit
            for i in range(month):
                filter_account.current_deposit += filter_account.uncredited_deposit * time_deposit_rate
            filter_account.balance += filter_account.current_deposit - org_current_deposit
            deposit.deposit_update_date = deposit.deposit_update_date + datetime.timedelta(days=month * 30)
            filter_account.save()
            deposit.save()
    print("定期存款更新结束")
    return None


# 后端启动时自动更新活期存款金额
def demand_deposit_record_update():
    print("开始更新活期存款金额")
    demand_deposit_rate = 0.0003
    today = datetime.datetime.now(tz=pytz.UTC)
    accounts = account.objects.all()
    for filter_account in accounts:
        delta_time = today - filter_account.uncredited_deposit_update_date
        month = int(delta_time.days / 30)
        for i in range(month):
            filter_account.uncredited_deposit += filter_account.uncredited_deposit * demand_deposit_rate
        filter_account.uncredited_deposit_update_date = (filter_account.uncredited_deposit_update_date
                                                         + datetime.timedelta(days=month*30))
        filter_account.save()
    print("活期存款更新结束")
    return None


@csrf_exempt
def cashier_unfreeze(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashierID'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无状态操作权限"}, status=403)
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_frozen = False
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def cashier_freeze(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashierID'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无状态操作权限"}, status=403)
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_frozen = True
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def cashier_reportloss(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashierID'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无状态操作权限"}, status=403)
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_lost = True
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def cashier_reissue(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        filter_cashier = cashier.objects.filter(cashier_id=data.get('cashierID'))
        if not filter_cashier.exists():
            return JsonResponse({"error": "柜员编号不存在"}, status=403)
        if not filter_cashier[0].manage_authority:
            return JsonResponse({"error": "柜员无状态操作权限"}, status=403)
        delete_account = account.objects.get(account_id = data.get("account"))
        old_id = delete_account.account_id
        new_account = account(
            password = delete_account.password,
            identity_card = delete_account.identity_card,
            phone_num = delete_account.phone_num,
            card_type = delete_account.card_type,
            balance = delete_account.balance,
            current_deposit = delete_account.current_deposit,
            uncredited_deposit = delete_account.uncredited_deposit,
            is_frozen = False,
            is_lost = False
        )
        new_account.save()
        new_id = new_account.account_id
        deposit_record.objects.filter(account_id = old_id).update(account_id = new_id)
        withdrawal_record.objects.filter(account_id = old_id).update(account_id = new_id)
        transfer_record.objects.filter(account_in_id = old_id).update(account_in_id = new_id)
        transfer_record.objects.filter(account_out_id = old_id).update(account_out_id = new_id)
        
        delete_account.delete()
        rs = {"accountID": new_id}
        return JsonResponse(rs, safe=False)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)