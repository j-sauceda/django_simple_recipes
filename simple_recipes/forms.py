from django.forms import ModelForm, ClearableFileInput
from django.contrib.auth.models import User
from .models import Article, ArticlePicture, Profile

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']


class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'
    exclude = ['user', 'date_joined']


class ArticleForm(ModelForm):
  class Meta:
    model = Article
    fields = '__all__'
    exclude = ['author']


class ArticlePictureForm(ModelForm):
  class Meta:
    model = ArticlePicture
    fields = '__all__'
    widgets = {
      'image': ClearableFileInput(attrs={'multiple': True}),
    }