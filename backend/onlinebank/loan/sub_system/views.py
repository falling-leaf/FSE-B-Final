from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import JsonResponse
from django.core import serializers
from . import models
import datetime
import json

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
                employee = models.employee.objects.get(employee_id=employee_id)


                loan_examiner = models.LoanExaminer(
                    employee_id=employee,
                    account=account,
                    other_information="add a new loan examiner at " + str(datetime.datetime.now())
                )
                loan_examiner.setPassword(password)
                loan_examiner.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully added information for loan examiner."
                print(type(response))
            elif operation == "update":
                loan_examiner_id = body.get("loan_examiner_id")
                new_password = body.get("new_password")

                loan_examiner = models.LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)
                loan_examiner.setPassword(new_password)
                loan_examiner.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully update loan examiner{loan_examiner_id} password."
            elif operation == "delete":
                loan_examiner_id = body.get("loan_examiner_id")
                loan_examiner = models.LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)
                employee = models.employee.objects.get(employee_id=loan_examiner.employee_id)

                employee.is_employeed = False
                employee.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully dismissal of a loan examiner{loan_examiner_id}."
            elif operation == "get":
                loan_examiner_id = body.get("loan_examiner_id")

                loan_examiner = models.LoanExaminer.objects.get(loan_examiner_id=loan_examiner_id)

                response['response_code'] = 1
                response['response_message'] = f"Successfully retrieved information for loan examiner {loan_examiner_id}."
                response['loan_examiner'] = serializers.serialize('json', loan_examiner)
            else:
                response['response_code'] = 0
                response['response_message'] = "Unrecognized operation type."

        except json.JSONDecodeError:
            response['response_code'] = 0
            response['response_message'] = "无效的JSON 负载"
        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)

    return JsonResponse(response)

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
                employee1 = models.employee.objects.get(employee_id=employee_id)

                loan_manager = models.LoanDepartmentManager(
                    employee_id=employee1,
                    account=account,
                    other_information="add a new loan examiner at " + str(datetime.datetime.now())
                )
                loan_manager.setPassword(password)
                loan_manager.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully added information for loan department manager."
            elif operation == "update":
                loan_manager_id = body.get("loan_manager_id")
                new_password = body.get("new_password")

                loan_manager = models.LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)
                loan_manager.setPassword(new_password)
                loan_manager.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully update loan manager{loan_manager_id} password."
            elif operation == "delete":
                loan_manager_id = body.get("loan_manager_id")
                loan_manager = models.LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)
                employee = models.employee.objects.get(employee_id=loan_manager.employee_id)

                employee.is_employeed = False
                employee.save()

                response['response_code'] = 1
                response['response_message'] = f"Successfully dismissal of a loan manager{loan_manager_id}."
            elif operation == 'get':
                loan_manager_id = body.get('loan_manager_id')
                loan_manager = models.LoanDepartmentManager.objects.get(loan_manager_id=loan_manager_id)

                response['response_code'] = 1
                response['response_message'] = f"Successfully retrieved information for loan manager{loan_manager_id}."
                response['loan_manager'] = serializers.serialize('json', loan_manager)
            else:
                response['response_code'] = 0
                response['response_message'] = "Unrecognized operation type."

        except Exception as e:
            response['response_code'] = 0
            response['response_message'] = str(e)

    return JsonResponse(response)
