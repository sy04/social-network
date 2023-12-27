from django import forms
from django.forms import ModelForm
from .models import Post, PostAttachment

class PostForm(ModelForm):
  body = forms.CharField(
      required=True,
      error_messages={
        'required': 'Body is required.',
      }
  )

  class Meta:
    model = Post
    fields = ('body', 'is_private')

class AttachmentForm(ModelForm):
  image = forms.ImageField(required=False)
  class Meta:
    model = PostAttachment
    fields = ('image',)

  def clean_avatar(self):
      avatar = self.cleaned_data.get('avatar')
      if avatar:
          # Validasi bahwa avatar adalah file
          if not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
              raise forms.ValidationError("Invalid file format. Please upload a valid image file.")
      return avatar

class PostListParams:
  def __init__(self, page: int = 1, limit: int = 10) -> None:
    self.page = page
    self.limit = limit