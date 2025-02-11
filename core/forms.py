from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # fields = ('title', 'description')
        fields = '__all__'

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        # }