from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, reverse
from datetime import datetime

from eventChart.models import (EventList)
# Create your views here.


# homepgae view 
class IndexView(View):
	template_name = 'index.html'
	
	def get_context_data(self):
		events = EventList.objects.filter(is_active=True, scheduled__gte = datetime.now()).order_by('created')[:3]
		return events

	def get(self, request):
		context = {
					'events' : self.get_context_data()
					}
		return render(request, self.template_name, context)