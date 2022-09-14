from django.contrib.auth.models import User
from django.db import models

from applications.base.models import TimeStampedModel, Delivery
from applications.products.models import Item, ItemOption


class CommonOrder(TimeStampedModel):
    """
    주문에 필요한 필드 생성을 위한 기본 모델
    """
    ORDER_STATUS = (
        ('ORDER', '주문'),
        ('CANCEL', '취소'),
    )
    order_status = models.CharField(verbose_name="주문 상태", choices=ORDER_STATUS, max_length=6)


class Order(CommonOrder):
    buyer = models.ForeignKey(
        User,
        verbose_name="구매자",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="buyer",
    )
    delivery = models.ForeignKey(
        Delivery,
        verbose_name="배송정보",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="주문",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="order",
    )
    order_item = models.ForeignKey(
        Item,
        verbose_name="주문 상품",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="order_item",
    )
    order_item_option = models.ForeignKey(
        ItemOption,
        verbose_name="주문 상품 옵션",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="order_item_option",
    )
    order_count = models.PositiveIntegerField(verbose_name="주문 수량")
