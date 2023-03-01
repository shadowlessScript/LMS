from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime,timedelta


#variables
online = 'online'
physical = 'physical'
both = 'physical/online'

active = 'active'
overDue = 'Over Due'
pending = 'Pending'
acquired = 'Acquired'
STATE = [
        (online, 'online'),
        (physical,'physical'),
        (both,'physical/online')
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
##### end of variable #####

# Create your models here.
# model for adding books
class AddBook(models.Model): 
    title = models.CharField(max_length=90) 
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
    copies = models.IntegerField(default=1)
    description = models.TextField(default=' ')
    Cover_image = models.ImageField(upload_to="images/books/%y", blank=True, null=True)
    type = models.CharField(max_length=20, choices=STATE, default='online')
    genre = models.CharField(max_length=50,choices=GENRE, default='Engineering')
    file = models.FileField(upload_to='books/%y', blank=True, null=True)

    def __str__(self):
        return '%s, %s'% (self.title, self.Author)

# Creating a news models, which will show news about the LIB SYS
class New(models.Model):
    title = models.CharField(max_length=90)
    story = QuillField(blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BorrowBook(models.Model):
    name_of_book = models.ForeignKey(AddBook, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    clients_name = models.OneToOneField(User, blank=True,null=True, on_delete=models.CASCADE)

    # add which user borrwed it
    def __str__(self):
        return str(self.name_of_book)

class Fine(models.Model):
    clients_name = models.ForeignKey(BorrowBook,blank=True,null=True, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.clients_name.clients_name.username}'

#class Booking(models.Model):
#    username = models.OneToOneField(User, blank=True,null=True, unique=False,on_delete=models.CASCADE)    
#    serial_number =  models.OneToOneField(AddBook, unique=False,on_delete=models.CASCADE )

#    def __str__(self):
#        return f'{self.username.username}'
class Booking(models.Model):

    # username = models.CharField(max_length=150, blank=False, null=False, default=' ')
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    serial_number = models.CharField(max_length=150, blank=False, null=False, default=' ')

    def __str__(self):
        return f'{self.username}'
# Adding a model for issuing books
def expiry():
    '''This function sets the expiry date for a book'''
    return datetime.today() + timedelta(days=15)

class IssueBook(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,)
    serial_number = models.ForeignKey(AddBook, on_delete=models.CASCADE,)
    status = models.CharField(max_length=20, choices=STATUS, default=active)
    issuedate = models.DateField(auto_now=True)
    due_date = models.DateField(default=expiry)

    
    def __str__(self):
        return f'{self.username.first_name} given {self.serial_number}'

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