from django.urls import path,include
from django.conf.urls import url

from applications.payment.views import (PlanListView,
							PlanCheckOutView,
							CreateCheckoutSessionView,
							stripe_webhook,
							StripeCancelView,
							StripeSuccessView
							)


urlpatterns	=	[
				# user account management
				path('plans/',PlanListView.as_view(),name='payment_plans'),
				path('checkout/<int:pk>/', PlanCheckOutView.as_view(),name='checkout'),
			
				path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
				path('webhooks/stripe', stripe_webhook, name='stripe_webhook'),
				path('stripe/status/cancel/', StripeCancelView.as_view(), name='stripe_cancel'),
				path('stripe/status/success/', StripeSuccessView.as_view(), name='stripe_success')

			]