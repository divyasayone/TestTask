from applications.payment.models import (Plan,PlanPurchaseHistory)
from applications.eventChart.models import (Event)
from datetime import datetime

from celery.app.utils import Settings
from Events.celery import app
def DeactivatePurchasePlanAfterExpiry():
    active_purchase_history = PlanPurchaseHistory.objects.select_related('owner').filter(expiry_date__lte=datetime.now(), has_paid=True, is_active=True)
    purchase_owners = active_purchase_history.values_list('owner_id', flat=True)
    active_events = Event.objects.filter(owner__in=purchase_owners, is_published=True).update(is_published=False)
    active_purchase_history.update(is_active=False)
  



DeactivatePurchasePlanAfterExpiry()





@app.task(bind=True)
def disable_expired_purchase(self, limit_per_run=50):
    active_purchase_history = PlanPurchaseHistory.objects.select_related('owner').filter(expiry_date__lte=datetime.now(), has_paid=True, is_active=True)
    purchase_owners = active_purchase_history.values_list('owner_id', flat=True)
    active_events = Event.objects.filter(owner__in=purchase_owners, is_published=True).update(is_active=False)
    active_purchase_history.update(is_active=False)
  