from django import forms
from collections import OrderedDict
from datetime import datetime
from eventChart.models import EventList

'''
    events addinmg and updating form
'''
class EventAddForm(forms.ModelForm):

    class Meta:
        model = EventList
        fields = '__all__'
        widgets = {
                    'scheduled' : forms.DateInput( attrs={ 'placeholder':'Select a date', 'type':'datetime-local'}),
                }

    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)
        fields_key_order = ['title', 'scheduled', 'venue', 'description', 'contact_number', 'contact_email', 'reference', 'more_info', 'promo_picture']
        
        if 'keyOrder' in self.fields:
            self.fields.keyOrder = fields_key_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)
        for k in self.visible_fields():
            k.field.widget.attrs['class'] = 'form-control'
    def clean(self):
        cleaned_data = super(EventAddForm, self).clean()
        scheduled_date = cleaned_data.get('scheduled',None)
        if scheduled_date and scheduled_date.replace(tzinfo=None) < datetime.now():
            raise forms.ValidationError({'scheduled': 'Enter a furutre date'})
