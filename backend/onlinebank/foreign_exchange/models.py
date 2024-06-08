from django.db import models

# Create your models here.
class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=80, unique=True)
    latest_exchange_buying_rate = models.DecimalField(max_digits=10, decimal_places=5)
    latest_exchange_selling_rate = models.DecimalField(max_digits=10, decimal_places=5)

    @staticmethod
    def GetCurrencyName(currencyId: int):
        currency = Currency.objects.get(currency_id=currencyId)
        return currency

class CurrencyHolding(models.Model):
    currency_holding_id = models.AutoField(primary_key=True)
    currency = models.ForeignKey('foreign_exchange.Currency', on_delete=models.CASCADE)
    online_user = models.ForeignKey('counteropt.online_user', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
        
    class Meta:
        unique_together = ('currency', 'online_user')

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            self.delete()
        else:
            super(CurrencyHolding, self).save(*args, **kwargs)

class ForeignExchangeOperator(models.Model):
    foreign_exchange_operator_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('counteropt.employee',on_delete=models.CASCADE)
    account = models.CharField(max_length=100, null = False, unique= True)
    password = models.CharField(max_length=80, null=False)
    alter_name_authority = models.BooleanField(default=False)
    alter_rate_authority = models.BooleanField(default=False)
    add_authority = models.BooleanField(default=False)
    delete_authority = models.BooleanField(default=False)

    class Meta:
        db_table = 'foreign_exchange_operator'
        ordering = ['foreign_exchange_operator_id'] 

    def __str__(self):
        return f"{self.foreign_exchange_operator_id}: {self.account}"
    
class ForeignExchangeTrading(models.Model):
    foreign_exchange_trading_id = models.AutoField(primary_key=True)
    account = models.ForeignKey('counteropt.account', on_delete=models.CASCADE)
    online_user = models.ForeignKey('counteropt.online_user', on_delete=models.CASCADE)
    currency = models.ForeignKey('foreign_exchange.Currency', on_delete=models.CASCADE)
    buy_or_sell = models.BooleanField(default=False)
    rmb_amount = models.DecimalField(max_digits=10, decimal_places=5)
    currency_amount = models.DecimalField(max_digits=10, decimal_places=5)
    trading_datetime = models.DateTimeField()

class RateUpdateRecord(models.Model):
    rate_update_record_id = models.AutoField(primary_key=True)
    currency = models.ForeignKey('foreign_exchange.Currency', on_delete=models.CASCADE)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=5)
    selling_rate = models.DecimalField(max_digits=10, decimal_places=5)
    update_datetime = models.DateTimeField()