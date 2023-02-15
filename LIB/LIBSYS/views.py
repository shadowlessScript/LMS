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
from django.contrib.admin.views.decorators import staff_member_required
from .models import New
# from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

# Create your views here.
def Notfound(request):
    return render(request, '404.html')


@staff_member_required
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

@staff_member_required(redirect_field_name='next', login_url=None)
def manageBook(request):
    Book = AddBook.objects.all()
    context = {'Books': Book}   
    return render(request, 'shelfs/manage.html', context)

@staff_member_required
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
    context['title']=update.title
    return render(request, 'shelfs/updates/updateBooks.html', context)

@staff_member_required
def deleteBook(request, serial_number):
    deleteBook = AddBook.objects.filter(serial_number=serial_number)
    context = {'Book': deleteBook}      
    return render(request, 'shelfs/updates/confirm_delete.html', context)
@staff_member_required
def deleteBookConfirmation(request, serial_number):
    deleteBook = AddBook.objects.filter(serial_number=serial_number)
    context = {'Book': deleteBook}
    messages.success(request, f'Book has been deleted')
    deleteBook.delete()

    return redirect('manage')

# news form down here
def index(request):
    News = New.objects.all()
    p = Paginator(New.objects.all(), 3)
    page = request.GET.get('page')
    posts = p.get_page(page)
    context = {
        'storys': posts,
        # 'pages': posts,
    }
    if request.user.is_superuser:
        return render(request,"mainAdmin.html", context)
    else:
        return render(request,"main.html", context)

@staff_member_required
def indexuserview(request):
    News = New.objects.all()
    context = {
        'storys': News,
    }    
    return render(request,"main.html", context)

def PostNews(request):
    if request.user.is_superuser:
        form = NewsForm()       
        context = {'blog': form}
         
        if request.method == 'POST': 
            form = NewsForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'News posted!')
                
            else:            
                messages.success(request, 'The news was not posted, please try again!')
    else:
        return render(request, '404.html')   
    return render(request, "news/News.html", context)


def NewsUpdate(request, id):
    if request.user.is_superuser:
        News = New.objects.get(id=id)
        form = NewsForm(instance=News) 
        context = {'blog': form}
         
        if request.method == 'POST': 
            form = NewsForm(request.POST, request.FILES, instance=News)
            if form.is_valid():
                form.save()
                messages.success(request, 'News Updated!')
                return redirect('home')
            else:            
                messages.success(request, 'The news was not updated, please try again!')
    else:
        return render(request, '404.html')   
    return render(request, "news/update/updateNews.html", context)


@login_required
def ListOfBooks(request):
    books = AddBook.objects.all()
    # genre = AddBook.objects.all()
    genre = []
    def genreList(lst):        
        lst = []
        for x in books:
            lst.append(x.genre)
            # print(lst)
        return set(lst)
    
    print(genreList(genre))
    return render(request, "shelfs/book.html", {
        'Books': books,
        'Genres': genreList(genre),
        })

@login_required
def bookView(request, serial_number):
    whichbook = AddBook.objects.filter(serial_number=serial_number)
    context = {'Book': whichbook}    
    return render(request, 'shelfs/bookview.html', context)


# creating a filter functionality
@login_required
def Filter(request, genre):
    book_filtered = AddBook.objects.filter(genre = genre)
    
    books = AddBook.objects.all()
    genre = []
    def genreList(lst):        
        lst = []
        for x in books:
            lst.append(x.genre)
            # print(lst)
        return set(lst)
    context = {
    'Book': book_filtered,
    'Genres': genreList(genre),
    }
    return render(request, 'shelfs/filter.html', context)

@login_required
def search_book(request):
    if request.method == 'POST':
        searched_books = request.POST['searched_books']  
        books = AddBook.objects.filter(title__contains=searched_books) 
        if books == []:
            print(books)     
        return render(request, 'search_books.html',{'searched': searched_books, 'Books': books})
    else:
        return render(request, 'search_books.html',{})

