from django.urls import path

from . import views

urlpatterns = [

    path('get_cards', views.get_cards),
    # 显示用户的所有卡
    path('new_application', views.new_application),
    # 用户申请信用卡
    path('get_application_at', views.get_application_at),
    # 用户查看自己的信用卡申请

    path('change_password', views.change_password),
    # 用户更改新密码
    path('frozen_card', views.frozen_card),
    # 用户冻结卡
    path('pay_to', views.pay_to),
    # 用户支付
    path('show_month_bill', views.show_month_bill),
    # 用户查看月账单
    path('update_limit', views.update_limit),
    # 用户更新信用卡余额
    path('cancel_card', views.cancel_card),
    # 用户取消卡
    path('repay', views.repay),
    # 用户还款
    path('lost_card', views.lost_card),
    # 挂失卡


    path('add_new_card', views.add_new_card),
    # 审核员新建卡
    path('get_check_applications', views.get_check_applications),  # 审核员看
    # 显示所有的申请
    path('get_uncheck_applications', views.get_uncheck_applications),  # 审核员看
    # 显示所有的申请
    path('change_application_state', views.change_application_state),
    # 审核申请

    path('add_examiner', views.add_examiner),
    # 添加信用卡审查员
    path('get_examiners', views.get_examiners),
    # 显示所有的审查员
    path('modify_examiner', views.modify_examiner),
    # 修改信用卡审查员信息
    path('grant_authority', views.grant_authority),
    # 授予权限
    path('revoke_authority', views.revoke_authority),
    # 收回权限
    path('delete_examiner', views.delete_examiner),
    # 删除信用卡审查员

]