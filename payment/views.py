from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, reverse
from datetime import datetime,timedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import stripe
from django.conf import settings
from django.views.generic import TemplateView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = settings.YOUR_DOMAIN
endpoint_secret = settings.WEBHOOK_SECRET_KEY

# from payments.forms import (EventAddForm)
from payment.models import (Plans,PlanPurchaseHistory)
## to add new  evemts 
 
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class PlansListView(View):
	# form_class = EventAddForm
	template_name = 'payments/pricing.html'
	success_url = 'newEvents'
	context = {}

	def get(self, request):
		plans = Plans.objects.all().order_by('price')
		current_plan	=	PlanPurchaseHistory.objects.filter(
			owner = request.user,
			is_active=True,
			expiry_date__gt = datetime.now()).first()
		self.context = {
			'plans' : plans,
			'current_plan' : current_plan,

		}
		return render(request, self.template_name, self.context)


@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class PlanCheckOutView(View):
	template_name = 'payments/checkout.html'
	context	=	{}
	instance	=	None
	
	def get(self, request, pk=None):
		self.instance	=	Plans.objects.filter(pk=pk).first()
		self.context = {
			'choosen_plan'	:	self.instance
		}
		return render(request, self.template_name, self.context)


'''
			reference
			# https://justdjango.com/blog/django-stripe-payments-tutorial
			# https://stripe.com/docs/checkout/quickstart
'''
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        plan = Plans.objects.get(id=self.kwargs["pk"])
        YOUR_DOMAIN = DOMAIN
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {	'price_data':	{
            			'currency': 'USD',
            			'unit_amount':	plan.price,
            			'product_data':{
            				'name':	plan.name
            			},
    				},
                    'quantity': 1,
                },
            ],
            metadata =	{
            	'package_plan': plan.id,
            	'active_period_days': plan.active_period_days,
              	'user_id': request.user.id,
            },
            customer_email = request.user.email,  
            mode = 'payment',
            success_url = YOUR_DOMAIN + '/payments/plans/',
            cancel_url = YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url)

@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Fulfill the purchase...
    fulfill_order(session)
  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Fulfill the purchase...
    fulfill_order(session)

  # Passed signature verification
  return HttpResponse(status=200)


def fulfill_order(session):
	
	stripe_intent = session["payment_intent"]
	user_id = session["metadata"]["user_id"]
	package = session["metadata"]["package_plan"]
	package_active_days	=	int(session["metadata"]["active_period_days"])
	expiry_date = datetime.now()+timedelta(package_active_days)
	new_obj, created = PlanPurchaseHistory.objects.update_or_create(
							owner_id=user_id,
							defaults = {
								'owner_id': user_id,
								'package_id':package,
								'has_paid':True,
								'is_active':True,
								'stripe_payment_intent':stripe_intent,
								'expiry_date' :expiry_date,
								}
							)
	
	# TODO: fill me in
	print("Fulfilling order")
	# Passed signature verification

class StripeCancelView(TemplateView):
	template_name =	"payments/stripe_cancel.html"

