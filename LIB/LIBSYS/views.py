from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import MemberForm
from django.contrib import messages
# Create your views here.
def signup(request):
    if request.method == "POST":        
        passwd = request.POST.get('passwd')
        passwd1 = request.POST.get('passwd1')
        form = MemberForm(request.POST or None)

        
        if form.is_valid():
            form.save()
            messages.success(request, "You have signed up successfully")
        return redirect("signup")
        # else:
        #     return HttpResponse("Passwords do not match")
    
    else:
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