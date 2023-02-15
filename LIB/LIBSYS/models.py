from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

online = 'online'
physical = 'physical'
both = 'physical/online'

STATE = [
        (online, 'online'),
        (physical,'physical'),
        (both,'physical/online')
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

# model for adding books
class AddBook(models.Model): 
    title = models.CharField(max_length=90) 
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
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


