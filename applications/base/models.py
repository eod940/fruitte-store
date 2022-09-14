from django.db import models

# 모델링에 들어가는 공통 요소 모델입니다.
from applications.orders.models import Order


class TimeStampedModel(models.Model):
    """
    생성일자, 수정일자 필드 생성을 위한 기본 모델
    """
    created_at = models.DateTimeField(verbose_name="생성일자", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일자", auto_now=True)

    class Meta:
        abstract = True


class DiscountOption:
    """
    할인 유형을 관리하기 위한 옵션들
    """
    DISCOUNT_OPTION_CHOICES = (
        ('PD', '기간할인'),  # Period Discount
        ('MD', '회원할인'),  # Member Discount
    )
    DISCOUNT_GRADE = (
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('B', 'Bronze'),
        ('A', 'All'),
    )

    class Meta:
        abstract = True


class Delivery(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="주문",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="order",
    )
    delivery_address = models.CharField(max_length=50)
