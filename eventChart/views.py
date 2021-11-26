from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse,JsonResponse

from eventChart.forms import (EventAddForm)
from eventChart.models import (EventList)
from payment.models import (PlanPurchaseHistory)

'''
 	to add new  evemts 
'''
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class AddNewEventView(View):
	form_class = EventAddForm
	template_name = 'events/add_events.html'
	success_url = 'myeventlist'
	instance = None
	def get(self, request, pk=None):
		if pk != None:
			self.instance	=	EventList.objects.filter(id=pk).first()
		return render(request, self.template_name, { 'form':  self.form_class(instance=self.instance) })

	def post(self, request, pk=None):
		if pk != None:
			self.instance	=	EventList.objects.filter(id=pk).first()
		form = self.form_class(request.POST, instance=self.instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.owner = request.user # update owner in event data
			instance.save()
			return redirect(reverse(self.success_url))

		return render(
	                request,
	                self.template_name,
	                { 'form': form, 'invalid_creds': True }
	            )

class EventListView(View):
	model_name	=	EventList
	template_name	=	'events/event_list.html'

	def get_context_data(self):
		events = EventList.objects.filter(is_active=True, scheduled_from__gte = datetime.now())
		return events

	def get(self, request):
		context = {
					'events_list' : self.get_context_data().order_by('scheduled_from'),
					'recent_list'	:	self.get_context_data().order_by('-created')
					}
		return render(request, self.template_name, context)

class EventDetailView(DetailView):
	model	=	EventList
	template_name	=	'events/event-details.html'

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class MyEventListview(View):
	template_name 	=	'events/myevents.html'
	context = {}
	
	def get_context_data(self):
		events = EventList.objects.filter(scheduled_from__gte = datetime.now(), owner = self.request.user)
		return events

	def get(self, request, pk=None):
		self.context = {
					'myevents' : self.get_context_data().order_by('scheduled_from'),
					}
		return render(request, self.template_name, self.context)

	def post(self, request , pk=None):
		if request.is_ajax():
			instance_id = request.POST.get('event_id',None)
			instance	=	EventList.objects.filter(id=instance_id).first().delete()
			self.context = {
				'status' :	200,
				"success" :	True,
			}
			return JsonResponse(self.context) 

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class ManageEventPublish(View):
	context = {}
	template_name = ''
	def post(self, request, pk=None):
		instance = EventList.objects.filter(pk=pk).first()
		activate_status = ['publish']
		inactivation_status = ['unpublish']
		action =  request.POST.get('event_action',None)
		current_plan = PlanPurchaseHistory.objects.filter(owner = request.user,
															is_active=True,
															expiry_date__gte=datetime.now()).last()
		active_events = EventList.objects.filter(is_active=True, scheduled_from__gte = datetime.now())
		pending_scope = 0
		if current_plan :
			pending_scope = current_plan.package.events_limit - active_events.count()

			if pending_scope <=0 and action not in inactivation_status:
				self.context = {
					'status' :	400,
					"success" :	False,
					"message"	: "Plan Limit exceeded,Please upgrade plan.",
					"redirect_url"	:	reverse('payment_plans'),
				}
			else:
				if request.is_ajax():
					
					if action in activate_status:
						instance.is_active = True
						message	=	"published"
						action =	'unpublish'
					elif action in inactivation_status:
						instance.is_active = False
						message	=	"unpublished"
						action	=	'publish'

					instance.save()
					self.context = {
						"status"	:	200,
						"success"	:	True,
						"message"	:	message,
						'action'	:	action,
					}
		else:
			self.context = {
					'status' :	400,
					"success" :	False,
					"message"	: "Please purchase a plan and publish.",
					"redirect_url"	:	reverse('payment_plans'),
				}

		return JsonResponse(self.context)
