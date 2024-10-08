from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from LIBSYS.models import Library
from PIL import Image
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, blank=True, null=True,on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="images/profile_pic/%y", default='images/profile_pic/22/default.jpg', blank=True, null=True)
	number = models.CharField(max_length=10,blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	affiliation = models.ForeignKey(Library, on_delete=models.CASCADE, default=None, blank=False, null=True) # WHICH LIBRARY BRANCH DOES THE CLIENTS BELONG TO?
	def __str__(self):
		return f'{self.user.username}'

class AdminProfile(models.Model):
	user = models.OneToOneField(User, blank=True, null=True,on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="images/profile_pic/%y", default='images/22/default.jpg', blank=True, null=True)
	number = models.CharField(max_length=10,blank=True, null=True)
	bio = models.TextField(blank=True, null=True)


	def __str__(self):
		return f'{self.user.username}'
