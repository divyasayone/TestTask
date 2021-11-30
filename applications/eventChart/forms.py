from django import forms
from collections import OrderedDict
from datetime import datetime
from applications.eventChart.models import Event

'''
    events addinmg and updating form
'''
class EventAddForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
                    'scheduled_from' : forms.DateInput( attrs={ 'placeholder':'Select a date', 'type':'datetime-local'}),
                    'scheduled_to' : forms.DateInput( attrs={ 'placeholder':'Select a date', 'type':'datetime-local'}),
                }
        labels = {
                "scheduled_to": "Scheduled upto (optional)",
                }

    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)
        fields_key_order = ['category','title', 'scheduled_from', 'scheduled_to', 'venue', 'description', 'contact_number', 'contact_email', 'reference', 'more_info', 'promo_picture',]
        
        if 'keyOrder' in self.fields:
            self.fields.keyOrder = fields_key_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)
        for k in self.visible_fields():
            k.field.widget.attrs['class'] = 'form-control'
    def clean(self):
        cleaned_data = super(EventAddForm, self).clean()
        scheduled_date = cleaned_data.get('scheduled_from',None)
        scheduled_to = cleaned_data.get('scheduled_to', None)
        category = cleaned_data.get('category', None)
        if not category :
            raise forms.ValidationError({'category': 'Choose an option'})
        if scheduled_date and scheduled_date.replace(tzinfo=None) < datetime.now():
            raise forms.ValidationError({'scheduled_from': 'Enter a furutre date'})
        if scheduled_to and scheduled_to.replace(tzinfo=None) < scheduled_date.replace(tzinfo=None):
            raise forms.ValidationError({'scheduled_to': 'Enter a furutre date to from date'})
