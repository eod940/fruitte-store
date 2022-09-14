from django.contrib import admin
from .models import Item, ItemOption, ItemImage, Discount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
