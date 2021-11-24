from django.shortcuts import render
from django.views import View

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from account.forms import (AuthenticationForm,RegisterForm)
# Create your views here.

'''

	 user login view using builtin AuthenticationForm form for easy use

'''
class UserLoginView(View):
	form_class = AuthenticationForm
	success_url  = 'Events'
	template_name 	=	'account/login.html'

	def get(self, request):
		return render(request, self.template_name, { 'form':  self.form_class })

	def post(self, request):
	    form = self.form_class(request, data=request.POST)
	    if form.is_valid():
	        user = authenticate(
	            request,
	            username=form.cleaned_data.get('username'),
	            password=form.cleaned_data.get('password')
	        )

	        if user is None:
	            return render(
	                request,
	                self.template_name,
	                { 'form': form, 'invalid_creds': True }
	            )

	        try:
	            form.confirm_login_allowed(user)
	        except ValidationError:
	            return render(
	                request,
	                self.template_name,
	                { 'form': form, 'invalid_creds': True }
	            )
	        login(request, user)

	        return redirect(reverse(self.success_url))
	    return render(
	                request,
	                self.template_name,
	                { 'form': form, 'invalid_creds': True }
	            )

'''

	 user logout view

'''
@method_decorator(login_required(login_url='/account/signin/'), name='dispatch')
class UserLogotView(View):
	success_url  = 'home'

	def get(self, request):
		logout(request)
		return redirect(reverse(self.success_url)) 

'''

	 user resitration view 

'''
class UserRegisterView(View):
	form_class = RegisterForm
	success_url  = 'signin'
	template_name 	=	'account/register.html'
	
	def get(self, request):

		return render(request, self.template_name, { 'form':  self.form_class })

	def post(self, request):
		form = self.form_class(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse(self.success_url))

		return render(
				request,
				self.template_name,
				{ 'form': form, 'invalid_creds': True }
			)