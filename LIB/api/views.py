from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UserSerializer, BookSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from LIBSYS.models import AddBook

@api_view(["GET"])
def getData(request):
	items = User.objects.all()
	serializer = UserSerializer(items, many=True)
	return Response(serializer.data)

@api_view(["POST"])
def mobileLogin(request):
	# return Response(request.data['username'])
	user = authenticate(request, username=request.data["username"], password=request.data["password"])
	if user is not None:		
		login(request, user)
		return Response("success")   
    	
	else:
		return HttpResponse("<h1>Wrong credentials!</h1>")

@api_view(["GET"])
def mobileLogOut(request):
	logout(request)
	return Response("success")

@api_view(["GET"])
def getBookData(request):
	items = AddBook.objects.all()
	serializer = BookSerializer(items, many=True)
	return Response(serializer.data)

@api_view(["GET"])
def getBookDetails(request, serial_number):
	items = AddBook.objects.filter(serial_number=serial_number)
	if items.exists():
		serializer = BookSerializer(items, many=True)
		return Response(serializer.data)
	else:
		return Response("Not found")
