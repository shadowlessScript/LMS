from django.db import models

# Create your models here.
class signupForm(models.Model):
    username = models.CharField(max_length=50)
    first_Name = models.CharField(max_length=50)
    last_Name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=100)
    Confirmpass = models.CharField(max_length=100)


    def __str__(self):
        return self.first_Name +" "+self.last_Name