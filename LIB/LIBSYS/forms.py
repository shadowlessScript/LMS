# from dataclasses import fie ld
from dataclasses import fields
from django import forms
from .models import New, AddBook,IssueBook, BookAcquisitionRequest, Exam, Rating
from django_quill.forms import QuillFormField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
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

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddBookForm(forms.ModelForm):
    # genre = forms.CharField(label='Book\'s genre', widget=forms.Select(choices=GENRE))
    class Meta:
        model = AddBook
        fields =('title', 'Author', 'serial_number', 'state','Cover_image','description','genre', 'ebook','copies')
        
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


class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssueBook
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-select'
        self.fields['isbn'].widget.attrs['class'] = 'form-select'
        self.fields['due_date'].disabled = True

class BookAcquisitionRequestForm(forms.ModelForm):
    class Meta:
        model = BookAcquisitionRequest
        fields = ('book_title', 'author', 'publisher')

    def __init__(self, *args, **kwargs):
        super(BookAcquisitionRequestForm, self).__init__(*args, **kwargs)
        self.fields['book_title'].widget.attrs['class'] = 'form-control'
        self.fields['author'].widget.attrs['class'] = 'form-control'
        self.fields['publisher'].widget.attrs['class'] = 'form-control'
        #self.fields['requester'].widget.hidden_widget()


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('unit_name', 'unit_code', 'year','type_of_exam','exam_file')

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['unit_name'].widget.attrs['class'] = 'form-control'
        self.fields['unit_code'].widget.attrs['class'] = 'form-control'
        self.fields['type_of_exam'].widget.attrs['class'] = 'bootstrap-select'


class ExtendBookForm(forms.ModelForm):
    class Meta:
        model = IssueBook
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ExtendBookForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['isbn'].widget.attrs['class'] = 'form-select'
        self.fields['username'].disabled = True
        self.fields['isbn'].disabled = True
        self.fields['status'].disabled = True
        # self.fields['due_date'].widget.attrs.update(input_type='date')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
