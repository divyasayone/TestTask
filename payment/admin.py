from django.contrib import admin

from payment.models import (
							Plans,
							PlanPurchaseHistory,)
# Register your models here.

admin.site.register(Plans)
admin.site.register(PlanPurchaseHistory)
