from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        passwd1 = request.POST.get('passwd1')

        if passwd == passwd1:
            myuser = User.objects.create_user(username, email, passwd)
            myuser.full_name = fname +" "+ lname
            myuser.save()
            messages.success(request, 'You have been registered successfully')
        else:
            return HttpResponse("Passwords do not match")
    return render(request, "signup.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user = User.objects.get(username=username)

    if user.check_password(passwd):
            return HttpResponse("success")
    else:
        return HttpResponse("Incorrect password or username")