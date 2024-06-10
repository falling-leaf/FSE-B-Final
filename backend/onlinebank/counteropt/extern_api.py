#这是为了给其他组调用接口的文件
from common.models import account
def balance_change(account_id, balance):
        target = account.objects.get(account_id = account_id)
        if target.balance - balance >= 0:
            target.balance = target.balance - balance
            return True
        else: return False