from django.urls import path,include
from django.conf.urls import url

from payment.views import (PlansListView,
							PlanCheckOutView,
							CreateCheckoutSessionView,
							stripe_webhook,
							StripeCancelView,
							)


urlpatterns	=	[
				# user account management
				path('plans/',PlansListView.as_view(),name='payment_plans'),
				path('checkout/<int:pk>/', PlanCheckOutView.as_view(),name='checkout'),
			
				path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
				path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
				path('stripe/status/', StripeCancelView.as_view(), name='stripe_cancel')
			]