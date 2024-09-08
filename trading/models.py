from django.db import models
from django_mysql.models import EnumField

from trading.common.enums import StrategyType, Broker, TradeState, OrderStatus, TxnType, OrderPriceType


class Strategy(models.Model):
    name = EnumField(choices=StrategyType)
    # todo: future roadmap: add performance metrics (ex: success rate, days win, trades win count)


class Trade(models.Model):
    strategy = models.ForeignKey(
        Strategy, on_delete=models.PROTECT,
        related_name='trades', related_query_name='trade',
        null=False,
    )
    broker = EnumField(choices=Broker, null=False)
    state = EnumField(choices=TradeState, null=False)
    day = models.DateField(null=False)
    initiation_time = models.TimeField(null=False)
    completion_time = models.TimeField(null=False)


class Order(models.Model):
    broker_txn_id = models.CharField(null=False)
    trade = models.ForeignKey(
        Trade, on_delete=models.PROTECT,
        related_name='orders', related_query_name='order',
        null=False,
    )
    txn_type = EnumField(choices=TxnType)
    instrument_symbol = models.CharField(null=False)
    qty = models.IntegerField(null=False)
    price_type = EnumField(choices=OrderPriceType, null=False)
    status = EnumField(choices=OrderStatus)
    order_request_time = models.TimeField(null=False)
    order_request_price = models.DecimalField(null=False)
    order_confirmation_time = models.TimeField(null=False)
    order_confirmation_price = models.DecimalField(null=False)
    tot_amount = models.DecimalField(null=False)
