# from dataclasses import fie ld
from dataclasses import fields
from django import forms
from .models import New, AddBook,IssueBook, BookAcquisitionRequest, Exam, Rating, BookReview
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
class UserDropdownField(forms.ModelChoiceField):
    # this removes the admin and staff from the list of users.
    def label_from_instance(self, user):
        return f"{user.get_full_name()} ({user.username})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = User.objects.filter(is_superuser=False, is_staff=False)
        self.queryset = queryset.order_by('username')

class PhysicalBookDropdownField(forms.ModelChoiceField):
    # this removes ebooks from the list of books that can be issued.
    def label_from_instance(self, book):
        return f"{book.title}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = AddBook.objects.filter(state__contains='print')
        self.queryset = queryset.order_by('title')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddBookForm(forms.ModelForm):
    # genre = forms.CharField(label='Book\'s genre', widget=forms.Select(choices=GENRE))
    class Meta:
        model = AddBook
        # fields =('title', 'Author', 'serial_number', 'state','Cover_image','description','genre', 'ebook','copies')
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['Author'].widget.attrs['class'] = 'form-control'
        self.fields['serial_number'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-select'
        self.fields['genre'].widget.attrs['class'] = 'form-select'
        self.fields['pages'].widget.attrs['class'] = 'form-control'
        self.fields['edition'].widget.attrs['class'] = 'form-control'
        self.fields['publisher'].widget.attrs['class'] = 'form-control'
        self.fields['co_authors'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['story'].widget.attrs['class'] = 'form-control'


class IssueBookForm(forms.ModelForm):
    username = UserDropdownField(queryset=User.objects.all())
    class Meta:
        model = IssueBook
        fields = "__all__"
    # isbn = forms.ModelChoiceField(queryset=AddBook.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    # due_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    isbn = PhysicalBookDropdownField(queryset=AddBook.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    username = UserDropdownField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)
        # self.fields['username'].disabled = True
        # self.fields['isbn'].widget.attrs['class'] = 'form-select'
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

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['review']

    
