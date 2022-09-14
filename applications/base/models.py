from django.db import models

# 모델링에 들어가는 공통 요소 모델입니다.


class TimeStampedModel(models.Model):
    """
    생성일자, 수정일자 필드 생성을 위한 기본 모델
    """
    created_at = models.DateTimeField(verbose_name="생성일자", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일자", auto_now=True)

    class Meta:
        abstract = True


class DiscountOption(models.Model):
    """
    할인 유형을 관리하기 위한 기본 모델
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
