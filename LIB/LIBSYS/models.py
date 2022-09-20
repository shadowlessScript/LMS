from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
# Create your models here.

# model for adding books
class AddBook(models.Model): 
    title = models.CharField(max_length=90) 
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
    description = models.TextField(default=' ')
    Cover_image = models.ImageField(upload_to="images/books/%y", blank=True, null=True)
    
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
    # add which user borrwed it
    def __str__(self):
        return self.name_of_book

