
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import UserForm,ProfileForm,RegisterUserForm
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            pass
            login(request, user)
            # Redirect to a success page.  
            return redirect('home')         
        else:
           messages.success(request,'There was an error logging in....')
           return redirect('login')
            # Return an 'invalid login' error message.
        
    else:
        return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,'You have logged out!')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            login(request, user)
            messages.success(request, 'Registration successfully')
            return redirect('home')
    else:
        form = RegisterUserForm()
        
    return render(request, 'authenticate/register_user.html',{
        'form': form,
        })


def profile(request):
    # user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=request.user)
        p_form = ProfileForm(request.POST or None,request.FILES,instance=request.user.profile)

        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, 'Updates')
            return redirect('profile')
        else:
            messages.success(request, 'Did not update ;(')
            return redirect('profile')
    else:
        
        form = UserForm(instance=request.user)           
        p_form = ProfileForm(instance=request.user.profile)
        
        # except:
        #     messages.success(request, 'User has no profile, contact the admin')
        #     return redirect('home')
        # else:
        #     messages.success(request, 'There was an error, contact the admin')
        #     return redirect('home')
    return render(request, 'profile/profile.html',{
        'form': form,
        'p_form': p_form,
        })
