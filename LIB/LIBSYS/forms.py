# from dataclasses import fie ld
from django import forms
from .models import New, AddBook
from django_quill.forms import QuillFormField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image
# from django.forms import ModelForm

from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddBookForm(forms.ModelForm):
    class Meta:
        model = AddBook
        fields ="__all__"
        
    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['Author'].widget.attrs['class'] = 'form-control'
        self.fields['serial_number'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = "__all__"