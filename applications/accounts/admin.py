from django.contrib import admin

# Register your models here.
from applications.accounts.models import User


@admin.register(User)
class AccountsAdmin(admin.ModelAdmin):
    pass
