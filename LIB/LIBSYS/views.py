from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from LIBSYS.models import signupForm
from .forms import AddBookForm
from .models import AddBook
from django.contrib import messages
# from django.contrib.auth.hashers import make_password

# Create your views here.
def signup(request):
    # form = UserCreationForm()
    # context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
        # form = MemberForm(request.POST or None)
    return render(request, "signup.html")

def login(request):
    if request.method == 'POST':
    #     username = request.POST.get('username')
    #     passwd = request.POST.get('password')
    #     user = signupForm.objects.get(username=username)

    # if user.check_password(passwd):
    #         return HttpResponse("success")
        pass
    else:
        return HttpResponse("Incorrect password or username")

def addBookstoShelf(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return render(request, 'shelfs/addbooks.html')
        else:
            messages.success(request, 'Something went wrong, please try again!')
            return render(request, 'shelfs/addbooks.html')

    return render(request, 'shelfs/addbooks.html')


def manageBook(request):
    Book = AddBook.objects.all()
    context = {'Books': Book}   
    return render(request, 'shelfs/manage.html', context)
    
def updateBook(request,serial_number):
    context = {}
    update  = AddBook.objects.get(pk=serial_number)
    form = AddBookForm(instance=update)
    if request.method == 'POST':
        form = AddBookForm(request.POST,instance=update)
        if form.is_valid():
            form.save()
            return redirect('manage')
    context['form']=form
    return render(request, 'shelfs/updateBooks.html', context)


def deleteBook(request, serial_number):
    delete = AddBook.objects.get(pk=serial_number)    
    delete.delete()
    messages.success(request, 'Something went wrong, please try again!')
    return redirect('manage')

