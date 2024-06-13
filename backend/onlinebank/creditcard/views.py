import json
from datetime import datetime
import pytz
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import account, online_user, CreditCardApplication, transfer_record, employee, CreditCardExaminer


# 信用卡操作部分---------------------------------------------------------------------------
@require_http_methods(["GET"])
def get_cards(request):
    """
    show all cards, return all credit cards
    """
    response = {}
    try:
        online_user_id = request.GET.get('online_user_id')
        if not online_user_id:
            raise ValueError("online_user_id is required")
        tz = pytz.timezone('Asia/Shanghai')
        cards = account.objects.filter(
            user_id=online_user_id,
            card_type=0,
        )
        formatted_cards = []
        for card in cards:
            formatted_cards.append({
                'account_id': card.account_id,
                'balance': card.balance,
                'credit_limit': card.credit_limit,
                'open_date': card.open_date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'is_lost': card.is_lost,
                'is_frozen': card.is_frozen,
            })
        response['status'] = 'success'
        response['message'] = 'Cards show successfully.'
        response['error_num'] = 0
        response['list'] = formatted_cards
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def add_new_card(request):
    """
    create a new card and return the card
    """
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        online_user_id = body.get('online_user_id')
        apply_id = body.get('apply_id')
        # print("in add_new_card")
        # print(apply_id)

        account().new_card(online_user_id, 0)

        # Change the application state of 'have_open'
        application = CreditCardApplication.objects.get(apply_id=apply_id)
        application.have_open = True
        application.save()

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Cards added successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    # Use JsonResponse to return the response dictionary as JSON
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """
    Change the password of a credit card and return the card
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body.get('account_id')
        new_password = body.get('new_password')
        old_password = body.get('old_password')

        # Fetch the credit card using the account_id from URL parameters
        card = account.objects.get(account_id=account_id)

        # Update the password
        card.modify_password(new_password, old_password)
        card.save()

        response['status'] = 'success'
        response['message'] = 'Password has been changed successfully.'
        response['error_num'] = 0
        response['card'] = serialize('json', [card], ensure_ascii=False)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    # Use JsonResponse to return the response dictionary as JSON
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def frozen_card(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = account.objects.get(account_id=account_id)
        card.frozen_card(password)

        response['status'] = 'success'
        response['message'] = 'New application has been created.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def update_limit(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = account.objects.get(account_id=account_id)

        card.update_credit_limit(password)

        response['status'] = 'success'
        response['message'] = 'Limit has been updated.'
        response['card'] = serialize('json', [card], ensure_ascii=False)
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def cancel_card(request):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body.get('account_id')
        password = body.get('password')
        card = account.objects.get(account_id=account_id)
        card.cancel_card(password)
        response['status'] = 'success'
        response['message'] = 'Card has been cancelled.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def repay(request):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body.get('account_id')  # 要还款的信用卡账户
        pay_account = body.get('pay_account')  # 支付的信用卡账户
        pay_password = body.get('pay_password')  # 支付的信用卡账户密码
        amount = float(body.get('amount'))
        print(account_id, pay_account, pay_password, amount)

        card = account.objects.get(account_id=account_id)
        pay_card = account.objects.get(account_id=pay_account)

        card.repay(pay_card, pay_password, amount)

        response['status'] = 'success'
        response['message'] = 'Payment has been completed.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def lost_card(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = account.objects.get(account_id=account_id)
        card.report_lost(password)
        response['status'] = 'success'
        response['message'] = 'Card has been reported lost successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 账单操作部分------------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(["POST"])
def pay_to(request):
    """
    add a record to the transfer_record
    """
    response = {}
    try:
        # 解析json
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_in_id = body.get('account_in_id')
        account_out_id = body.get('account_out_id')
        amount = float(body.get('amount'))
        password = body.get('password')

        # update the balance of payer and receiver
        in_card = account.objects.get(account_id=account_in_id)
        out_card = account.objects.get(account_id=account_out_id)
        if in_card == out_card:
            raise ValueError("收款方和付款方不能相同")
        in_card.transfer_in(amount)
        out_card.transfer_out(amount, password)

        # update the information in transaction
        new_transaction = transfer_record(
            account_in_id=body.get('account_in_id'),
            account_out_id=body.get('account_out_id'),
            transfer_amount=body.get('amount'),
            transfer_date=datetime.now().strftime('%Y-%m-%d')  # 使用当前时间作为交易日期
        )
        new_transaction.save()

        response['status'] = 'success'
        response['message'] = 'New transaction has been created and saved successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_month_bill(request):
    response = {}
    try:
        year = request.GET.get('year')
        month = request.GET.get('month')
        account_id = request.GET.get('account_id')
        if not account_id:
            raise ValueError("账号传递失败")
        if not year or not month:
            raise ValueError("请输入年月")  # Year and month parameters are required.

        # Define your timezone (Asia/Shanghai)
        tz = pytz.timezone('Asia/Shanghai')

        # Create timezone-aware start and end dates
        start_date = datetime(int(year), int(month), 1)
        if month == '12':
            end_date = datetime(int(year) + 1, 1, 1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1)

        start_date = make_aware(start_date, timezone=tz)
        end_date = make_aware(end_date, timezone=tz)

        in_bill = transfer_record.objects.filter(
            account_in_id=account_id,
            transfer_date__gte=start_date,
            transfer_date__lt=end_date
        )
        out_bill = transfer_record.objects.filter(
            account_out_id=account_id,
            transfer_date__gte=start_date,
            transfer_date__lt=end_date
        )

        # Calculate total in and out amounts
        in_total_amount = in_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0
        out_total_amount = out_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0

        # Prepare bills list for custom formatting
        bills = list(in_bill) + list(out_bill)
        formatted_bills = []
        for bill in bills:
            formatted_bills.append({
                'transfer_record_id': bill.transfer_record_id,
                'account_in_id': bill.account_in_id,
                'account_out_id': bill.account_out_id,
                'transfer_amount': bill.transfer_amount,
                'transfer_date': bill.transfer_date.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Response setup
        response['total_amount'] = in_total_amount - out_total_amount
        response['in_amount'] = in_total_amount
        response['out_amount'] = out_total_amount
        response['list'] = formatted_bills
        # response['list'] = json.loads(serializers.serialize('json', formatted_bills))
        response['status'] = 'success'
        response['message'] = 'All bills have been saved.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 信用卡审核员部分----------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(["POST"])
def add_examiner(request):
    """
    get employee_id, add a new examine, return the examiner
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        employee_name = body.get('employee_name')
        identity_card = body.get('identity_card')
        phone_number = body.get('phone_number')
        password = body.get('password')
        other_information = body.get('other_information')
        account_ = body.get('account')
        sex = body.get('sex')
        if CreditCardExaminer.objects.filter(account=account_).exists():
            return JsonResponse({"error": "该信用卡审查员账户已存在"}, status=403)

        employee_sex_ = 0
        if sex == 'female':
            employee_sex_ = 1

        new_employee = employee(
            employee_name=employee_name,
            identity_card=identity_card,
            employee_sex=employee_sex_,
            phone_number=phone_number,
            occupation_name='信用卡审查员',
            is_employeed=True,
            other_information=other_information
        )
        new_employee.save()

        new_examiner = CreditCardExaminer(
            employee=new_employee,
            account=account_,  # Example account name generation
            password=password,
            check_authority=1  # default grant the authority
        )
        new_examiner.save()

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Examiner added successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_examiners(request):
    """
    show all examiners
    """
    response = {}
    try:
        examiners = CreditCardExaminer.objects.all()
        examiner_info = []
        for examiner in examiners:
            employee_ = employee.objects.get(employee_id=examiner.employee_id)
            if employee_.employee_sex == 0:
                sex = '男'
            else:
                sex = '女'
            examiner_info.append({
                'examiner_id': examiner.credit_examiner_id,
                'employee_name': employee_.employee_name,
                'account': examiner.account,
                'phone_number': employee_.phone_number,
                'check_authority': examiner.check_authority,
                'sex': sex,
                'employee_id': employee_.employee_id,
            })
        response['status'] = 'success'
        response['message'] = 'Examiners show successfully.'
        response['error_num'] = 0
        response['list'] = examiner_info
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def modify_examiner(request):
    """
    Modify an existing examiner's information(account & password)
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
        # Get the new information
        new_account = body.get('new_account')
        new_password = body.get('new_password')
        new_employee_name = body.get('new_employee_name')
        new_identity_card = body.get('new_identity_card')
        new_phone_number = body.get('new_phone_number')
        new_other_information = body.get('new_other_information')
        new_sex = body.get('new_sex')

        if new_sex == 'female':
            new_sex = 0
        if new_sex == 'male':
            new_sex = 1

        # Update the password
        examiner.modify_examiner_info(new_account, new_password)
        examiner.save()

        employee_ = employee.objects.get(employee_id=examiner.employee_id)
        employee_.other_information = new_other_information
        employee_.phone_number = new_phone_number
        employee_.sex = new_sex
        employee_.identity_card = new_identity_card
        employee_.name = new_employee_name
        employee_.save()

        response['status'] = 'success'
        response['message'] = 'Examiner info has been modified successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def grant_authority(request):
    """
    Grant an existing examiner the authority to examine
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
        # Set authority
        examiner.grant()
        examiner.save()

        response['status'] = 'success'
        response['message'] = 'Grant authority successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def revoke_authority(request):
    """
    Revoke the authority of an existing examiner
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
        # Revoke authority
        examiner.revoke()
        examiner.save()

        response['status'] = 'success'
        response['message'] = 'Revoke authority successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def delete_examiner(request):
    """
    Delete an existing examiner
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
        examiner.delete()
        response['status'] = 'success'
        response['message'] = 'Examiner has been deleted successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 申请管理部分-----------------------------------------------------------------------------------------
@require_http_methods(["GET"])
def get_check_applications(request):
    """
    show all checked applications, return all applications
    """
    response = {}
    try:
        tz = pytz.timezone('Asia/Shanghai')
        applications = CreditCardApplication.objects.filter(apply_status=1)
        formatted_applications = []
        for application in applications:
            online_user_ = online_user.objects.get(user_id=application.online_user_id)
            if online_user_.service_year >= 20:
                s = (online_user_.service_year * 20 + 0.0001 * online_user_.annual_income / 20 +
                     0.0002 * online_user_.property_valuation / 20)
            else:
                s = (online_user_.service_year * online_user_.service_year +
                     0.0001 * online_user_.annual_income / online_user_.service_year +
                     0.0002 * online_user_.property_valuation / online_user_.service_year)
            if s >= 320:
                credit = '优秀'
            elif s >= 250:
                credit = '良好'
            elif s >= 150:
                credit = '一般'
            else:
                credit = '较差'

            formatted_applications.append({
                'apply_id': application.apply_id,
                'apply_status': application.apply_status,
                'apply_result': application.apply_result,
                'apply_date': application.apply_date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'examiner_id': application.creditCardExaminer_id,
                'online_user_id': application.online_user_id,
                'have_open': application.have_open,
                'credit': credit,
            })
        response['status'] = 'success'
        response['message'] = 'Applications show successfully.'
        response['error_num'] = 0
        response['list'] = formatted_applications
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_uncheck_applications(request):
    """
    show all applications, return all applications
    """
    response = {}
    try:
        tz = pytz.timezone('Asia/Shanghai')
        applications = CreditCardApplication.objects.filter(apply_status=0)
        formatted_applications = []

        for application in applications:

            online_user_ = online_user.objects.get(user_id=application.online_user_id)
            if online_user_.service_year >= 20:
                s = (online_user_.service_year * 20 + 0.0001 * online_user_.annual_income / 20 +
                     0.0002 * online_user_.property_valuation / 20)
            else:
                s = (online_user_.service_year * online_user_.service_year +
                     0.0001 * online_user_.annual_income / online_user_.service_year +
                     0.0002 * online_user_.property_valuation / online_user_.service_year)
            if s >= 350:
                credit = '优秀'
            elif s >= 250:
                credit = '良好'
            elif s >= 150:
                credit = '一般'
            else:
                credit = '较差'

            formatted_applications.append({
                'apply_id': application.apply_id,
                'apply_status': application.apply_status,
                'apply_result': application.apply_result,
                'apply_date': application.apply_date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'examiner_id': application.creditCardExaminer_id,
                'online_user_id': application.online_user_id,
                'credit': credit,
            })
        response['status'] = 'success'
        response['message'] = 'Applications show successfully.'
        response['error_num'] = 0
        response['list'] = formatted_applications
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def new_application(request):
    """
    User applies for a new credit card application, and return the application details.
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        online_user_id = body.get('online_user_id')
        annual_income = float(body.get('annual_income'))
        property_valuation = float(body.get('property_valuation'))
        service_year = int(body.get('service_year'))

        if not online_user_id:
            raise ValueError("online_user_id is required")

        online_user_ = online_user.objects.get(user_id=online_user_id)
        online_user_.annual_income = annual_income
        online_user_.property_valuation = property_valuation
        online_user_.service_year = service_year
        online_user_.save()

        # Create a new application using the obtained online_user
        CreditCardApplication().new_apply(online_user_id)

        response['status'] = 'success'
        response['message'] = 'New application has been created.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_application_at(request):
    """
    User gets his own application details
    """
    response = {}
    try:
        online_user_id = request.GET['online_user_id']
        applications = CreditCardApplication.objects.filter(online_user=online_user_id)
        tz = pytz.timezone('Asia/Shanghai')
        format_applications = []
        for application in applications:
            format_applications.append({
                'apply_id': application.apply_id,
                'apply_status': application.apply_status,
                'apply_result': application.apply_result,
                'apply_date': application.apply_date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                'examiner_id': application.creditCardExaminer_id,
                'have_open': application.have_open,
            })
        response['status'] = 'success'
        response['message'] = 'Get applications successfully.'
        response['list'] = format_applications
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def change_application_state(request):
    """
    Examiner change the state of a credit card application
    """
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        apply_id = body.get('apply_id')
        # print(f"Received apply_id: {apply_id}")  # 调试输出

        if not apply_id:
            raise ValueError("apply_id is required")

        # 确保 apply_id 转换为整数
        apply_id = int(apply_id)
        apply = CreditCardApplication.objects.get(apply_id=apply_id)

        # Get the result and examiner_id
        apply_result = body.get('apply_result')
        examiner_id = int(body.get('examiner_id'))
        if not examiner_id:
            raise ValueError("examiner_id is required")
        print("in view = ")
        print(examiner_id)

        # Update the apply_status and apply_result
        apply.change_state(apply_result, examiner_id)
        apply.save()

        response['status'] = 'success'
        response['message'] = 'The application has been examined.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
