from django.db import models
from django_mysql.models import EnumField

from trading.common.enums import StrategyType, Broker, TradeState, OrderStatus, TxnType, OrderPriceType


class Strategy(models.Model):
    name = EnumField(choices=StrategyType.choices())
    # todo: future roadmap: add performance metrics (ex: success rate, days win, trades win count)


class Trade(models.Model):
    strategy = models.ForeignKey(
        Strategy, on_delete=models.PROTECT,
        related_name='trades', related_query_name='trade',
        null=False,
    )
    broker = EnumField(choices=Broker.choices(), null=False)
    state = EnumField(choices=TradeState.choices(), null=False)
    day = models.DateField(null=False)
    initiation_time = models.TimeField(null=False)
    root_stoploss = models.DecimalField(null=True)
    completion_time = models.TimeField(null=False)


class Order(models.Model):
    broker_txn_id = models.CharField(null=False, max_length=50)
    trade = models.ForeignKey(
        Trade, on_delete=models.PROTECT,
        related_name='orders', related_query_name='order',
        null=False,
    )
    txn_type = EnumField(choices=TxnType.choices())
    instrument_symbol = models.CharField(null=False, max_length=50)
    qty = models.IntegerField(null=False)
    price_type = EnumField(choices=OrderPriceType.choices(), null=False)
    status = EnumField(choices=OrderStatus.choices())
    order_request_time = models.TimeField(null=False)
    order_request_price = models.DecimalField(null=False, decimal_places=2, max_digits=7)
    order_confirmation_time = models.TimeField(null=False)
    order_confirmation_price = models.DecimalField(null=False, decimal_places=2, max_digits=7)
    tot_amount = models.DecimalField(null=False, decimal_places=2, max_digits=8)
