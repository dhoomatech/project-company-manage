from django.contrib import admin
from django.apps import apps
from .models import *

# Register your models here.


apps = apps.get_app_config('payments_management')

# for model_name, model in apps.models.items():
#     admin.site.register(model)


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['id','tittle' ,'paid_amount','from_user','is_active']
admin.site.register(Transactions, TransactionsAdmin)


class MembershipPackAdmin(admin.ModelAdmin):
    list_display = ['id','tittle' ,'amount','expire_days']
admin.site.register(MembershipPack, MembershipPackAdmin)


class userCardDataAdmin(admin.ModelAdmin):
    list_display = ['id','user' ,'token','is_active']
admin.site.register(userCardData, userCardDataAdmin)


class SubscriptionListAdmin(admin.ModelAdmin):
    list_display = ['id','user' ,'package','created']
admin.site.register(SubscriptionList, SubscriptionListAdmin)


class PaymentTransationAdmin(admin.ModelAdmin):
    list_display = ['id','phone' ,'paid_amount','transaction_id']
admin.site.register(PaymentTransation, PaymentTransationAdmin)