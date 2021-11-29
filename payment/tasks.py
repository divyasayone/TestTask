from payment.models import (Plans,PlanPurchaseHistory)
from eventChart.models import (EventList)
from datetime import datetime

def DeactivatePurchasePlanAfterExpiry():
    active_purchase_history = PlanPurchaseHistory.objects.select_related('owner').filter(expiry_date__lte = datetime.now(), has_paid = True, is_active=True)
    purchase_owners = active_purchase_history.values_list('owner_id', flat=True)
    active_events = EventList.objects.filter(owner__in=purchase_owners, is_active=True).update(is_active = False)
    active_purchase_history.update(is_active = False)
  



DeactivatePurchasePlanAfterExpiry()