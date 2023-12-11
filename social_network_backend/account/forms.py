from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForms(UserCreationForm):
  email = forms.EmailField(
      required=True,
      error_messages={
          'invalid': 'Enter a valid email address.',
          'required': 'Email is required.',
      }
  )

  name = forms.CharField(
      max_length=30,
      required=True,
      error_messages={
          'required': 'Name is required.',
          'max_length': 'Name must not exceed 30 characters.',
      }
  )

  password1 = forms.CharField(
      min_length=8,
      required=True,
      error_messages={
          'required': 'Password is required.',
          'max_length': 'Password min 8 characters.',
      }
  )

  password2 = forms.CharField(
      min_length=8,
      required=True,
      error_messages={
          'required': 'Password confirmation is required.',
          'max_length': 'Password confirmation min 8 characters.',
      }
  )

  class Meta:
    model = User
    fields = ('email', 'name', 'password1', 'password2')

  def clean_password2(self):
      password1 = self.cleaned_data.get('password1')
      password2 = self.cleaned_data.get('password2')
      if password1 and password2 and password1 != password2:
          raise forms.ValidationError("Passwords do not match.")
      return password2

class ProfileForms(forms.ModelForm):
  email = forms.EmailField(
      required=True,
      error_messages={
          'invalid': 'Enter a valid email address.',
          'required': 'Email is required.',
      }
  )

  name = forms.CharField(
      max_length=30,
      required=True,
      error_messages={
          'required': 'Name is required.',
          'max_length': 'Name must not exceed 30 characters.',
      }
  )

  avatar = forms.ImageField(required=False)

  class Meta:
    model = User
    fields = ('email', 'name', 'avatar')

  def clean_avatar(self):
      avatar = self.cleaned_data.get('avatar')
      if avatar:
          # Validasi bahwa avatar adalah file
          if not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
              raise forms.ValidationError("Invalid file format. Please upload a valid image file.")
      return avatar