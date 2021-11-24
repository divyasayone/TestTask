from django.db import models
from datetime import datetime
from account.models import User
# Create your models here.
'''
for user events CRUD 
'''
class EventList(models.Model):
	def event_promotion_image(self,filename,):
		 return 'event/images/%s/%s' % (self.owner.id, filename)

	title	=	models.CharField(max_length = 100)
	description	=	models.TextField(blank=True)
	scheduled	=	models.DateTimeField()
	venue	=	models.CharField(max_length=100,blank=True)
	promo_picture	=	models.FileField(blank=True,null=True,upload_to = event_promotion_image)
	contact_number	=	models.CharField(max_length=50)
	contact_email	=	models.EmailField(blank=True,null=True)
	reference	=	models.URLField(max_length = 200)
	more_info	=	models.TextField(blank=True,null=True)
	owner	=	models.ForeignKey(User,on_delete=models.CASCADE)
	is_active	=	models.BooleanField(default=False) ## deactivate after expiry or as per user need
	created	=	models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.title[:10] 

