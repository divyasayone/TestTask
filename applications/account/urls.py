from django.conf.urls import url
from django.urls import path,include


from applications.account.views import (UserLoginView,
                            UserLogotView,
                            UserRegisterView,)


urlpatterns = [
	# basic user account management (reg,login and logout)
    path('signup/', UserRegisterView.as_view(), name='register'),
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('logout/', UserLogotView.as_view(), name='logout'),


	]