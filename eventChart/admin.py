from django.contrib import admin

from eventChart.models import (Event,EventCategory)
# Register your models here.

admin.site.register(Event)
admin.site.register(EventCategory)