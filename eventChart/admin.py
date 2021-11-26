from django.contrib import admin

from eventChart.models import (EventList,EventCategory)
# Register your models here.

admin.site.register(EventList)
admin.site.register(EventCategory)