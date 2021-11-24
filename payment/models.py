from django.db import models
from datetime import datetime

from account.models import User
# Create your models here.

class Plans(models.Model):
	name	=	models.CharField(max_length=100)
	details	=	models.TextField(blank=True,null=True)
	price	=	models.IntegerField(default=1000) # in cents
	active_period_days	=	models.IntegerField(default=30)
	events_limit	=	models.IntegerField(default=1)
	created	=	models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.name

	def get_formated_price(self):
		return "{0:.2f}".format( self.price / 100 )

class PlanPurchaseHistory(models.Model):
	package	=	models.ForeignKey(Plans, on_delete = models.CASCADE, verbose_name = 'package')
	owner	=	models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'owner' , unique = True)
	purchase_date	=	models.DateTimeField(default=datetime.now, blank=True)
	expiry_date	=	models.DateTimeField(default=datetime.now, blank=True)
	is_active	=	models.BooleanField(default = True)
	stripe_payment_intent = models.CharField(max_length=200, blank=True, null=True)
	has_paid = models.BooleanField(default=False, verbose_name='Payment Status')

	def __str__(self):
		return self.owner.first_name + "-" + self.package.name



