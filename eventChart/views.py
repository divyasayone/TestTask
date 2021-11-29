from django.views import View,generic
from django.urls import reverse_lazy

from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.http import Http404
from django.http import HttpResponse,JsonResponse
from django.conf import settings

from eventChart.forms import (EventAddForm)
from eventChart.models import (Event,EventCategory)
from payment import models
from payment.models import (PlanPurchaseHistory)

'''
 	to add new  evemts 
'''
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class AddEventView(SuccessMessageMixin,generic.CreateView):
	form_class = EventAddForm
	template_name = 'events/add_events.html'
	success_url = reverse_lazy('newevent')
	success_message = "Added successfully"

	
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(AddEventView, self).form_valid(form)

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class UpdateEventView(SuccessMessageMixin,generic.UpdateView):
	model = Event
	form_class = EventAddForm
	template_name = 'events/add_events.html'
	success_url = reverse_lazy('myevents')
	success_message = "updated successfully"

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class DeleteEventView(generic.DeleteView):
	model = Event
	success_url = reverse_lazy('myevents')

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(DeleteEventView, self).get_object()
		if not obj.owner == self.request.user:
			raise Http404
		return obj
	
	def post(self, request, *args, **kwargs):
		queryset = self.get_object()
		queryset.delete()
		self.context = {
				'status' :	200,
				"success" :	True,
			}
		return JsonResponse(self.context) 

		pass

@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class MyEventView(generic.ListView):
	model	=	Event
	template_name	=	'events/myevents.html'
	paginate_by = settings.EVENT_PAGINATION_LIMIT
	context_object_name = 'myevents'
	
	def get_queryset(self):
		return Event.objects.filter(scheduled_from__gte = datetime.now(), owner = self.request.user).order_by('created')
		return context

class EventListView(generic.ListView):
	model	=	Event
	template_name	=	'events/event_list.html'
	paginate_by = settings.PAGINATION_LIMIT

	def get_queryset(self):
		filter_val = self.request.GET.get('filter', None)
		order = self.request.GET.get('orderby', 'scheduled_from')
		events = Event.objects.filter(is_published=True,
										scheduled_from__gte = datetime.now(),
										).order_by(order)
		if filter_val:
			events = events.filter(category__name = filter_val)
		return	events

	def get_context_data(self, **kwargs):
		context = super(EventListView, self).get_context_data(**kwargs)
		if 'Event_list' in context and context['Event_list']:
			context['events_list'] = context['Event_list']
			context['recent_list'] = context['Event_list'][::-1]
			context['categories'] = EventCategory.objects.all()
	

class EventDetailView(generic.DetailView):
	model	=	Event
	template_name	=	'events/event-details.html'
	context_object_name = 'event'
	
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class ManageEventPublish(generic.UpdateView):
	model = Event
	instance = None
	activate_status = ['publish']
	inactivation_status = ['unpublish']
	
	def get_object(self, *args, **kwargs):
		self.instance = super(ManageEventPublish, self).get_object(*args, **kwargs)
		if not self.instance.owner == self.request.user:
			raise Http404 # maybe you'll need to write a middleware to catch 403's same way
		return self.instance
		
	def post(self, request, *args, **kwargs):
		self.get_object()
		action =  request.POST.get('event_action',None)
		current_plan = PlanPurchaseHistory.objects.filter(owner = request.user,
															is_active=True,
															expiry_date__gte=datetime.now()).last()
		active_events = Event.objects.filter(is_published=True,
											scheduled_from__gte = datetime.now(),
											owner = request.user, )
		pending_scope = 0
		if current_plan :
			pending_scope = current_plan.package.events_limit - active_events.count()

			if pending_scope <=0 and action not in self.inactivation_status:
				self.context = {
					'status' :	400,
					"success" :	False,
					"message"	: "Plan Limit exceeded,Please upgrade plan.",
					"redirect_url"	:	reverse('payment_plans'),
				}
			else:
				if request.is_ajax():
					
					if action in self.activate_status:
						self.instance.is_published = True
						message	=	"published"
						action =	'unpublish'
					elif action in self.inactivation_status:
						self.instance.is_published = False
						message	=	"unpublished"
						action	=	'publish'

					self.instance.save()
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
