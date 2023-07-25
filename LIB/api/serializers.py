from rest_framework import serializers
from django.contrib.auth.models import User
from LIBSYS.models import AddBook

class UserSerializer(serializers.ModelSerializer):
		class Meta:
			model = User 
			fields = ("username", "password")

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddBook
		fields = "__all__"