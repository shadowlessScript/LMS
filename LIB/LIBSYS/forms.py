# from dataclasses import fie ld
from django import forms
from .models import New, signupForm, AddBook
from django_quill.forms import QuillFormField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.forms import ModelForm

from django import forms
class MemberForm(forms.ModelForm):
    class Meta:
        model = signupForm
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddBookForm(forms.ModelForm):
    class Meta:
        model = AddBook
        fields = "__all__"

class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = "__all__"