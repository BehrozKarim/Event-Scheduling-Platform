from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from betterforms.multiform import MultiModelForm

from .models import Event

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EventForm(forms.ModelForm):


    class Meta:
        model = Event
        fields = ['type', 'title', 'organizer', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }



class EventCreateMultiForm(MultiModelForm):
    form_classes = {
        'event': EventForm,
    }