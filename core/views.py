from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, reverse
from datetime import datetime

from eventChart.models import (Event)
# Create your views here.


# homepgae view 
class IndexView(View):
	template_name = 'index.html'
	
	def get_context_data(self):
		events = Event.objects.filter(is_published=True, scheduled_from__gte = datetime.now()).order_by('created')[:3]
		return events

	def get(self, request):
		context = {
					'events' : self.get_context_data()
					}
		return render(request, self.template_name, context)

class TestView(View):
	template_name = 'test.html'
	context = {}
	
	def get(self, request):


		from payment import tasks as t
		t.DeactivatePurchasePlanAfterExpiry()



		return render(request, self.template_name, self.context)