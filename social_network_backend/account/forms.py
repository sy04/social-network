from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForms(UserCreationForm):
  class Meta:
    model = User
    fields = ('email', 'name', 'password1', 'password2')

class ProfileForms(forms.ModelForm):
  class Meta:
    model = User
    fields = ('email', 'name', 'avatar')