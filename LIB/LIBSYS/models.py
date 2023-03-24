from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.core.validators import MaxValueValidator, MinValueValidator


#variables
online = 'ebook'
physical = 'physical'
both = 'physical/ebook'

active = 'active'
overDue = 'Over Due'
pending = 'Pending'
acquired = 'Acquired'
STATE = [
        (online, online),
        (physical,physical),
        (both,both)
    ]

STATUS = [
        (active, 'Active'),
        (overDue, 'Over Due')
    ]

REQUEST_STATUS = [
        (pending, 'Pending'),
        (acquired, 'Acquired')
    ]

GENRE = [
    ('Engineering',(
        ('Civil Engineering','Civil Engineering' ),
        ('Software Engineering','Software Engineering'), 
        ('Computer Science','Computer Science')
        )
        ),
    ('Economics',(
        (' Classical economics',' Classical economics'),
        ('Neo-classical economics','Neo-classical economics')
        )

        ),
    ('Novel','Novel'),
    ('Science','Science'),
    ('Business','Business'),
    ('Mathematics','Mathematics'),

]

main_exam = "Main exam"
cat = "CAT"

TYPE_OF_EXAM = [
    (main_exam, main_exam),
    (cat, cat)
    ]
##### end of variable #####

# Create your models here.
# model for adding books
class AddBook(models.Model): 
    title = models.CharField(max_length=90) 
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
    copies = models.IntegerField(default=1)
    copies_remaining = models.IntegerField(default=1)
    description = models.TextField(default=' ')
    Cover_image = models.ImageField(upload_to="images/books/%y", blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE, default='online')
    genre = models.CharField(max_length=50,choices=GENRE, default='Engineering')
    ebook = models.FileField(upload_to='books/%y', blank=True, null=True)

    def __str__(self):
        return '%s, %s'% (self.title, self.Author)

# Creating a news models, which will show news about the LIB SYS
class New(models.Model):
    title = models.CharField(max_length=90)
    story = QuillField(blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Fine(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,)
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE,)    
    # issuedate = models.DateField(auto_now=True)
    due_date = models.DateField(auto_now=True)
    over_due_by = models.IntegerField(default = 10)
    price = models.IntegerField(default = 10)

    def __str__(self):
        return f'{self.username}'

class Booking(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    isbn = models.ForeignKey(AddBook, on_delete=models.CASCADE,)

    def __str__(self):
        return f'{self.username}'
# Adding a model for issuing books
def expiry():
    '''This function sets the expiry date for a book'''
    return datetime.today() + timedelta(days=15)

class IssueBook(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,)
    isbn = models.ForeignKey(AddBook, on_delete=models.CASCADE,)
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
    #exam_title = models.CharField(max_length=150, blank=False, null=False)
    unit_name =  models.CharField(max_length=150, blank=False, null=False)
    unit_code =  models.CharField(max_length=150, blank=False, null=False)
    year = models.IntegerField()
    type_of_exam =  models.CharField(max_length=150, choices=TYPE_OF_EXAM, default=main_exam)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_file = models.FileField(upload_to='exams/%y', blank=True, null=True)

    def __str__(self):
        return f"{self.unit_name} {self.unit_code}, {self.type_of_exam}, {self.year}"

class Rating(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(AddBook, on_delete=models.CASCADE)
    rate = models.FloatField(default=0, validators=[ MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return "%s, %s, %s" % (self.username, self.book.title, self.rate)
