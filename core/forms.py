from django import forms
from .models import Event, EventImage

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = ('title', 'description')
        fields = '__all__'

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        # }

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ('image',)

EventImageFormSet = forms.modelformset_factory(EventImage, form=EventImageForm, extra=3)