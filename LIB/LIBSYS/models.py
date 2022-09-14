from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
# Create your models here.
class signupForm(models.Model):

    username = models.CharField(max_length=50, primary_key=True)
    first_Name = models.CharField(max_length=50)
    last_Name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=100)
    # Confirmpass = models.CharField(max_length=100)


    def __str__(self):
        return self.first_Name +" "+self.last_Name


# model for adding books
class AddBook(models.Model):
    title = models.CharField(max_length=90)
    Author = models.CharField(max_length=50)
    serial_number = models.CharField(primary_key=True, max_length=100)
    description = models.TextField(default=' ')

    def __str__(self):
        return self.title + "---"+self.Author

# Creating a news models, which will show news about the LIB SYS
class New(models.Model):
    title = models.CharField(max_length=90)
    story = QuillField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
