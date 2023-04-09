
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import UserForm,ProfileForm,RegisterUserForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
import requests
import json
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:            
            login(request, user)
            # Redirect to a success page.  
            return redirect('home')         
        else:
           messages.success(request,'Incorrect username or password')
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
            messages.success(request, 'Profile Update successful!')
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

@login_required
def payfine(request):
    x = Profile.objects.filter(user=request.user)
    for c in x:
        phonenumber = c.number
    # cl = MpesaClient()
    # # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    # phone_number = phonenumber
    # amount = 1
    # account_reference = 'reference'
    # transaction_desc = 'Pay your fine!'
    # callback_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    # r = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query' 
    # response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    # result = cl.stk_push(phone_number, amount, account_reference, transaction_desc, r)
    # print([x for x in response])
    # # return HttpResponse(response)
    # data = request.body

    # return HttpResponse(response, result)

    # initiate transcation using tinypesa
    url = "https://tinypesa.com/api/v1/express/initialize" # API endpoint for tinypesa
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "ApiKey": "4OzXOaySC7S"
    }

    payload = {
        'amount': 1,
        'msisdn': phonenumber,
        "callback_url": "https://your-callback-url.com" 
        
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:  # check if the request was successful
        data = response.json()  # get the JSON response data
        return HttpResponse(data)  # print the response data
    else:
        return HttpResponse(f"Error: {response.status_code}")  # print the error code if the request was unsuccessful



@login_required
def patronlookup(request, username):
    patron = User.objects.get(username=username)
    patron_profile = Profile.objects.filter(id=patron.profile.id)
    # print(patron.profile.id)
    return render(request, 'profile/patronlookup.html', {'patron':patron_profile})