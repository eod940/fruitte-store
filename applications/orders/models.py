from django.db import models

from applications.accounts.models import User
from applications.base.models import TimeStampedModel
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

    class Meta:
        abstract = True


class Order(CommonOrder):
    """
    주문 관리를 위한 모델입니다.
    """
    DELIVERY_STATUS = (
        ('READY', '준비중'),
        ('COMP', '완료'),  # Complete
    )
    buyer = models.ForeignKey(
        User,
        verbose_name="구매자",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="buyer",
    )
    delivery = models.CharField(verbose_name="배송정보", choices=DELIVERY_STATUS, max_length=6)

    class Meta:
        verbose_name = "주문"
        db_table = "orders"

    def __str__(self):
        return f'구매자: {self.buyer}'


class OrderItem(models.Model):
    """
    주문 상품을 위한 모델입니다.
    """
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

    class Meta:
        verbose_name = "주문 상품"
        db_table = "order_ items"

    def __str__(self):
        return f'{self.order}, {self.order_item_option}'
