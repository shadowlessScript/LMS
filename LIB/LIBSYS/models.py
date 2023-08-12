from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.admin import UserAdmin
from .HelperVar import *
from PIL import Image
from django_resized import ResizedImageField
from LIB.settings import BASE_DIR


# from django.contrib.auth.models import User


# ----------------- models ----------------------
# TODO: - Table Addbook normalization.
#       - Book model (title, serial number).
#       - Book Details, which will contain the rest of the fields.
#       - add ISBN and eISBN field, I may need to customize the save function depending on the book state.
#       - Create a library model, and make it a foreign key in the book model.

class Library(models.Model):
    name = models.CharField(max_length=100)

    # repository = models.ManyToManyField(Book, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} Library'


class Book(models.Model):
    title = models.CharField(max_length=90)
    serial_number = models.CharField(max_length=100, primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


class BookDetail(models.Model):
    """
        Holds the book's details
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    copies = models.IntegerField(default=1)
    copies_remaining = models.IntegerField(default=1)
    description = models.TextField(default=' ')
    cover_image = ResizedImageField(size=[200, 200], upload_to="images/books/%y", blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE, default='online')
    genre = models.CharField(max_length=50, choices=GENRE, default='Engineering')
    ebook = models.FileField(upload_to='books/%y', blank=True, null=True)
    pages = models.IntegerField()
    edition = models.CharField(max_length=50, default='first edition', blank=False, null=False)
    publisher = models.CharField(max_length=150, default='Nami printers', blank=False, null=False)
    co_authors = models.CharField(max_length=240, blank=True, null=True)
    year = models.CharField(max_length=150)
    call_number = models.CharField(max_length=150)
    ISBN = models.CharField(max_length=150, null=True, blank=True)
    eISBN = models.CharField(max_length=150, null=True, blank=True)

    # Adding a custom save function
    def save(self, *args, **kwargs):

        super().save(*args, *kwargs)


class AddBook(models.Model):
    title = models.CharField(max_length=90)
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
    copies = models.IntegerField(default=1)
    copies_remaining = models.IntegerField(default=1)
    description = models.TextField(default=' ')
    Cover_image = models.ImageField(upload_to="images/books/%y", blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE, default='online')
    genre = models.CharField(max_length=50, choices=GENRE, default='Engineering')
    ebook = models.FileField(upload_to='books/%y', blank=True, null=True)
    pages = models.IntegerField()
    edition = models.CharField(max_length=50, default='first edition', blank=False, null=False)
    publisher = models.CharField(max_length=150, default='Nami printers', blank=False, null=False)
    co_authors = models.CharField(max_length=240, blank=True, null=True)
    year = models.CharField(max_length=150, default='2010')
    call_number = models.CharField(max_length=150, default="PR 6302 C6 R56")

    def __str__(self):
        return '%s, %s' % (self.title, self.Author)


# Creating a news models, which will show news about the LIB SYS
class New(models.Model):
    # TODO: CHANGE IT NAME FROM NEW TO SOMETHING ELSE
    title = models.CharField(max_length=90)
    story = QuillField(blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Fine(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE, )
    # issuedate = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=FINESTATUS, default='Unpaid')
    due_date = models.DateField(default=datetime.today())
    over_due_by = models.IntegerField(default=10)
    price = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.username}'


class Booking(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    isbn = models.ForeignKey(AddBook, on_delete=models.CASCADE, )  # TODO: Change to serial number

    def __str__(self):
        return f'{self.username}'


# Adding a model for issuing books
def expiry():
    """ This function sets the expiry date for a book """
    return datetime.today() + timedelta(days=15)


def filter_out_admin():
    return User.objects.filter(staff_status=False)


class IssueBook(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    isbn = models.ForeignKey(AddBook, on_delete=models.CASCADE, )  # TODO: Change to serial number
    status = models.CharField(max_length=20, choices=STATUS, default=active)
    issuedate = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=expiry)

    def __str__(self):
        return f'{self.username.first_name} given {self.isbn}'


class ReturnedBook(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE, )
    return_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.serial_number}'


class BookAcquisitionRequest(models.Model):
    book_title = models.CharField(max_length=150, blank=False, null=False)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150, blank=False, null=False)
    requester = models.CharField(max_length=150, blank=False, null=False, default=' ')
    status = models.CharField(max_length=30, choices=REQUEST_STATUS, default=pending)

    def __str__(self):
        return f'{self.book_title} requested'


class Exam(models.Model):
    # exam_title = models.CharField(max_length=150, blank=False, null=False)
    unit_name = models.CharField(max_length=150, blank=False, null=False)
    unit_code = models.CharField(max_length=150, blank=False, null=False)
    year = models.IntegerField()
    type_of_exam = models.CharField(max_length=150, choices=TYPE_OF_EXAM, default=main_exam)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_file = models.FileField(upload_to='exams/%y', blank=True, null=True)

    def __str__(self):
        return f"{self.unit_name} {self.unit_code}, {self.type_of_exam}, {self.year}"


class Rating(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE)
    rate = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return "%s, %s, %s" % (self.username, self.serial_number.title, self.rate)


class Bookmark(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(AddBook, on_delete=models.CASCADE)


class History(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now=True)


class BookReview(models.Model):
    book = models.ForeignKey(AddBook, related_name='reviews', on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review = QuillField()
    created = models.DateTimeField(auto_now_add=True)
