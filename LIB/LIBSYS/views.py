from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from .forms import AddBookForm, NewsForm
from .models import AddBook
from django.contrib import messages
# from django.contrib.auth.hashers import make_password

# Create your views here.
def addBookstoShelf(request):
    
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('add')
        else:
            messages.success(request, 'Something went wrong, please try again!')
            return redirect('add')
    else:
        form = AddBookForm()
    return render(request, 'shelfs/addbooks.html', {"form":form})


def manageBook(request):
    Book = AddBook.objects.all()
    context = {'Books': Book}   
    return render(request, 'shelfs/manage.html', context)
    
def updateBook(request,serial_number):
    context = {}
    update  = AddBook.objects.get(pk=serial_number)
    form = AddBookForm(instance=update)
    if request.method == 'POST':
        form = AddBookForm(request.POST,request.FILES,instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, f'{form.cleaned_data["title"]} has been updated!')
            return redirect('manage')
        else:
            messages.success(request, f'{form.cleaned_data["title"]} has not been updated, please try again!')
    context['form']=form
    return render(request, 'shelfs/updates/updateBooks.html', context)


def deleteBook(request, serial_number):
    delete = AddBook.objects.get(pk=serial_number)    
    delete.delete()
    messages.success(request, 'Something went wrong, please try again!')
    return redirect('manage')

# news form down here

def NewsUpdate(request):
    form = NewsForm() 
    context = {'blog': form}
     
    if request.method == 'POST': 
        form = NewsForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'News posted!')
            
        else:            
            messages.success(request, 'The news was not posted, please try again!')   
    return render(request, "news/News.html", context)

def ListOfBooks(request):
    books = AddBook.objects.all()
    return render(request, "shelfs/book.html", {
        'Books': books,
        })


def bookView(request, serial_number):
    whichbook = AddBook.objects.filter(serial_number=serial_number)
    context = {'Book': whichbook}
    
    return render(request, 'shelfs/bookview.html', context)