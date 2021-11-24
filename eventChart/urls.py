from django.urls import path,include
from django.conf.urls import url

from eventChart.views import (
					AddNewEventView,
					EventListView,
					EventDetailView,
					MyEventListview,
					ManageEventPublish,)
					


urlpatterns	=	[
		# user account management
	    path('add/new/',AddNewEventView.as_view(),name='newEvents'),
	    path('edit/<int:pk>/', AddNewEventView.as_view(),name='editEvents'),


	    path('list/',EventListView.as_view(),name='Events'),
	    path('detail/<int:pk>', EventDetailView.as_view(), name='event-detail'),

	    path('manage/', MyEventListview.as_view(), name='myeventlist'),
	    path('delete/<int:pk>/', MyEventListview.as_view(), name='deletemyevent'),

	    path('publish/<int:pk>/', ManageEventPublish.as_view(), name='publishevent'),
	    path('unpublish/<int:pk>/', ManageEventPublish.as_view(), name='unpublishevent'),

	]