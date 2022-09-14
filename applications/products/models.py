from django.core.validators import MaxValueValidator
from django.db import models
from applications.base.models import TimeStampedModel, DiscountOption


# 상품 관리를 위한 모델입니다.


class CommonItemModel(TimeStampedModel):
    """
    상품명, 수량, 가격 필드 생성을 위한 기본 모델입니다.
    """
    item_name = models.CharField(verbose_name="상품명", max_length=30)
    item_stock = models.PositiveIntegerField(
        verbose_name="상품수량",
        default=0,
        validators=[MaxValueValidator(99)]  # 최대 수량은 99개로 제한함
    )
    item_supply_price = models.PositiveIntegerField(verbose_name="공급가격", default=0)
    item_retail_price = models.PositiveIntegerField(verbose_name="소비자가", default=0)
    item_sale_price = models.PositiveIntegerField(verbose_name="판매가", default=0)
    item_text = models.CharField(verbose_name="상품설명", max_length=250)
    item_content = models.TextField(verbose_name="상세설명")
    is_item_sale = models.BooleanField(verbose_name="판매여부", default=False)
    is_item_discount = models.BooleanField(verbose_name="할인여부", default=False)

    class Meta:
        abstract = True


class Item(CommonItemModel):
    """
    하나의 개별 상품을 관리하기 위한 모델입니다.
    """
    class Meta:
        verbose_name = "단일상품"
        db_table = "items"

    def __str__(self):
        return f'{self.item_name}'


class ItemOption(models.Model):
    """
    상품의 추가적인 옵션을 관리하기 위한 모델입니다.
    """
    option_name = models.CharField(verbose_name="옵션명", max_length=30, help_text="무게, 용량 등")
    option_value = models.CharField(verbose_name="옵션값", max_length=30, help_text="판매 단위")
    option_extra_price = models.IntegerField(verbose_name="옵션 추가금액", default=0)
    option_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="option",
    )

    class Meta:
        verbose_name = "아이템 옵션"
        db_table = "item_options"

    def __str__(self):
        return f'({self.option_item})--{self.option_value}'


class ItemImage(TimeStampedModel):
    """
    상품의 이미지를 관리하기 위한 모델입니다.
    """
    image_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="image",
    )
    head_image = models.ImageField(
        verbose_name="상품 이미지",
        blank=True,
        upload_to="item/item_head_image/%Y/%m"
    )
    detail_image = models.ImageField(
        verbose_name="상품 상세 이미지",
        blank=True,
        upload_to="item/item_detail_image/%Y/%m"
    )

    class Meta:
        verbose_name = "상품 이미지"
        db_table = "item_images"

    def __str__(self):
        return f'{self.origin_name}'


class Discount(models.Model):
    """
    할인 관리를 위한 모델입니다.
    base.models 에서 공통사항을 수정할 수 있습니다.
    """
    is_proceeding = models.BooleanField(verbose_name="할인 진행중", default=False)
    discount_option = models.CharField(
        verbose_name="할인 유형",
        choices=DiscountOption.DISCOUNT_OPTION_CHOICES,
        default="MD",
        max_length=5,
    )
    discount_title = models.CharField(verbose_name="할인명", max_length=50)
    discount_start = models.DateTimeField(verbose_name="할인 시작")
    discount_finish = models.DateTimeField(verbose_name="마감 기간")
    discount_target = models.CharField(
        verbose_name="할인적용범위",
        choices=DiscountOption.DISCOUNT_GRADE,
        default="A",
        max_length=10,
    )
    discount_rate = models.PositiveIntegerField(
        verbose_name="할인률(정률, %)",
        validators=[MaxValueValidator(99)]  # 최대 할인율은 99%로 제한함
    )
    discount_value = models.PositiveIntegerField(
        verbose_name="할인액(정액, 원)",
    )

    class Meta:
        db_table = "discounts"
        verbose_name = "할인 이벤트"

    def __str__(self):
        return f'{self.discount_title} - {self.discount_finish}까지'
