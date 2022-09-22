# from dataclasses import fie ld
from django import forms
from .models import New, AddBook
from django_quill.forms import QuillFormField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image
from .models import GENRE
# GENRE = [
#     ('Engineering','Engineering'),
#     ('Economics','Economics'),
#     ('Novel','Novel'),
#     ('Science','Science'),
#     ('Business','Business'),
#     ('Mathematics','Mathematics'),

# ]


# from django.forms import ModelForm

from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddBookForm(forms.ModelForm):
    # genre = forms.CharField(label='Book\'s genre', widget=forms.Select(choices=GENRE))
    class Meta:
        model = AddBook
        fields =('title', 'Author', 'serial_number', 'type','Cover_image','description','genre')
        
    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['Author'].widget.attrs['class'] = 'form-control'
        self.fields['serial_number'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        # self.fields['genre'].widget.attrs['class'] = 'btn-check'
        # self.fields['genre'].widget.attrs['id'] = 'btn-check'
        # self.fields['genre'].widget.attrs['type'] = 'radio'


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['story'].widget.attrs['class'] = 'form-control'

