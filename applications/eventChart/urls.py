from django.urls import path
from django.conf.urls import url

from applications.eventChart.views import (

	AddEventView,
	UpdateEventView,
	DeleteEventView,
	EventListView,
	EventDetailView,
	MyEventView,
	ManageEventPublish,	
	CategoryNameAutocomplete,
)
					

urlpatterns = [
	path('add/new/', AddEventView.as_view(), name='newevent'),
	path('edit/<int:pk>/', UpdateEventView.as_view(), name='editevent'),
	path('delete/<int:pk>/', DeleteEventView.as_view(), name='deleteevent'),
	path('manage/', MyEventView.as_view(), name='myevents'),

	path('list/', EventListView.as_view(), name='eventslist'),
	path('detail/<int:pk>', EventDetailView.as_view(), name='event-detail'),

	path('publish/<int:pk>/', ManageEventPublish.as_view(), name='publishevent'),
	path('unpublish/<int:pk>/', ManageEventPublish.as_view(), name='unpublishevent'),

	url(r'^category-autocomplete/$', CategoryNameAutocomplete.as_view(), name='category-autocomplete',),

]