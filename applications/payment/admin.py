from django.contrib import admin

from applications.payment.models import (
							Plan,
							PlanPurchaseHistory,)
# Register your models here.

admin.site.register(Plan)
admin.site.register(PlanPurchaseHistory)
