from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from .forms import AddBookForm, NewsForm, IssueBookForm, BookAcquisitionRequestForm, ExamForm, ExtendBookForm
from .models import AddBook,New, Booking, IssueBook, BookAcquisitionRequest, ReturnedBook, Exam, Fine
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from scholarly import scholarly, ProxyGenerator

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
            buf = form.save(commit=False)
            buf.copies_remaining = form.cleaned_data['copies']
            buf.save()
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
    p = Paginator(New.objects.all().order_by('created'), 3)
    page = request.GET.get('page')
    posts = p.get_page(page)
    request_status = BookAcquisitionRequest.objects.filter(requester = request.user)
    context = {
        'storys': posts,
        'request_status': request_status,
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

@staff_member_required
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

@staff_member_required
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
    p = Paginator(books.order_by('title'), 10)
    page = request.GET.get('page')
    b = p.get_page(page)
    # genre = AddBook.objects.all()
    genre = []
    def genreList(lst):        
        lst = []
        for x in books:
            lst.append(x.genre)
            # print(lst)
        return set(lst)
    
    # print(genreList(genre))
    return render(request, "shelfs/book.html", {
        'Books': b,
        'Genres': genreList(genre),
        })

@login_required
def bookView(request, serial_number):
    if request.method == 'POST':
        # this sends a booking request, will be saved in the Booking model

        try:
            booking = Booking(username=request.user, isbn_id=request.POST.get('isbn'))
            print(f'---> {booking}')
            booking.save()
            messages.success(request, 'Book request sent')
        except:
            messages.success(request, 'Something went wrong ;(')

    whichbook = AddBook.objects.filter(serial_number=serial_number)
    # print(whichbook[0].Author)
    context = {'Book': whichbook}
    try:
        search_query = scholarly.search_author(f'{whichbook[0].Author}')
        author = scholarly.fill(next(search_query))
        strip_author = author['publications']
        # print(strip_author)
        counter = 0
        pub = []
        citedby = []
        num = []

        for k in strip_author:
            if counter < 4:
                for v in k:
                    if v == 'bib':
                        pub.append(k[v])

                    elif  v == 'citedby_url':
                        citedby.append(k[v])

                    elif v == 'num_citations':
                        num.append(k[v])
            else:
                break
            counter += 1
        context['pub'] = pub
        context['citedby'] = citedby
        context['num'] = num
        # print(save_dict)
    except:
        pass



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
# end of filter function

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

@login_required
def dashboard(request):
    request_counter = Booking.objects.count()
    start_date = date.today()
    end_date = start_date - timedelta(days=7)
    book = AddBook.objects.all()
    number_of_books = 0
    for x in book:
        number_of_books += int(x.copies)
    return render(request, 'dashboard/dashboard.html', {
        'counter':request_counter,
        'number_of_books': number_of_books,
        'fines': Fine.objects.count(),
        'BAR': BookAcquisitionRequest.objects.count(), # BAR --> BookAcquisitionRequest
        'books_issued': IssueBook.objects.filter(issuedate__range=(end_date, start_date)).count(),

        })
    
@staff_member_required               
def booking(request):
    booking_request = Booking.objects.all()
    bookings = {'requests': booking_request}
    return render(request, 'dashboard/booking.html', bookings)

@staff_member_required
def issuebookrequest(request, id, isbn):
    bookrequest = Booking.objects.get(id=id) 
    form = IssueBookForm(instance=bookrequest)
    con = {'check':bookrequest}

    context = {}
    context['form'] = form  
    if request.method == 'POST':
        form = IssueBookForm(request.POST)        
        if form.is_valid():           
            buf = form.save(commit=False) # hold from saving the posted info
            if buf.isbn.copies > 0:
                # condition for checking number of copies and decrementing
                
                book = AddBook.objects.filter(serial_number=form.cleaned_data['isbn'].serial_number)
                for x in book:
                    x.copies -=  1
                    x.save()
                    #print(x.copies)
                buf.save()
                patron = form.cleaned_data['username']
                mails = User.objects.get(username=patron).email
                print(mails)
                send_mail(
                    f'{form.cleaned_data["isbn"]}',
                    f' Hi {patron}, you have been given {form.cleaned_data["isbn"]}, the due date is {form.cleaned_data["due_date"]}',
                    'settings.EMAIL_HOST_USER',
                    [mails],
                    fail_silently=False
                    )
                messages.success(request, f'{form.cleaned_data["isbn"]} has been given to {form.cleaned_data["username"]}')
            else:
                messages.success(request, "No more books are available in the DB how is this possible")
        return redirect('IssueBook')
    return render(request, 'dashboard/IssueBook.html', context)

@staff_member_required
def issueBook(request):
    if request.method == 'POST':       
        form = IssueBookForm(request.POST)        
        if form.is_valid():
            buf = form.save(commit=False) # hold from saving the posted info
            if buf.serial_number.copies > 0:
                # condition for checking number of copies and decrementing
                
                book = AddBook.objects.filter(serial_number=form.cleaned_data['serial_number'].serial_number)
                for x in book:
                    x.copies -=  1
                    x.save()
                    #print(x.copies)
                buf.save()
                patron = form.cleaned_data['username']
                mails = User.objects.get(username=patron).email
                print(mails)
                send_mail(
                    f'{form.cleaned_data["serial_number"]}',
                    f' Hi {patron}, you have been given {form.cleaned_data["serial_number"]}, the due date is {form.cleaned_data["due_date"]}',
                    'settings.EMAIL_HOST_USER',
                    [mails],
                    fail_silently=False
                    )
                messages.success(request, f'{form.cleaned_data["serial_number"]} has been given to {form.cleaned_data["username"]}')
            else:
                messages.success(request, "No more books are available in the DB how is this possible")
            
            
            return redirect('IssueBook')
    else:
        form = IssueBookForm()
    context = {}
    context['form'] = form
    return render(request, 'dashboard/IssueBook.html', context)

@staff_member_required
def viewIssuedBooks(request):
   issuedBooks = IssueBook.objects.filter(status = 'active')
   p = Paginator(issuedBooks.order_by('issuedate'), 10)
   page = request.GET.get('page')
   b = p.get_page(page)
   context = {
       'issues': b,
       }
   return render(request, 'dashboard/viewIssued.html', context)

@staff_member_required
def overdue(request):
   issuedBooks = IssueBook.objects.filter(status = 'Over Due')
   context = {
       'issues':issuedBooks,
       }
   return render(request, 'dashboard/overdue.html', context)

@login_required
def bookAcquisitionRequest(request):
    if request.method == 'POST':
        form = BookAcquisitionRequestForm(request.POST)
        
        if form.is_valid(): 
            buf = form.save(commit=False)
            buf.requester = request.user
            buf.save()
            messages.success(request, 'Request has been sent!')
            return redirect('bookacquire')

        else:
            print(form)
            messages.success(request, 'Something went wrong!')
            return redirect('bookacquire')
    else:
        context = {}
        form = BookAcquisitionRequestForm()
        context['form'] = form
    return render(request, 'bookacquire.html', context)

@staff_member_required
def getthisbook(request):
    
    requests = BookAcquisitionRequest.objects.all()
    return render(request, 'dashboard/getthisbook.html', {'requests':requests})

@staff_member_required
def questCompleted(request, id):
    quest = BookAcquisitionRequest.objects.get(id=id)
    quest.status='Acquired'
    quest.save()
    return redirect('getthisbook')

@staff_member_required
def returnedBook(request, id):
    # the book's details are moved to return book model and deleted from IssueBook model
    book = IssueBook.objects.get(id=id)

    returned = ReturnedBook(username=book.username, serial_number=book.serial_number)
    returned.save()
    # patron = book.username
    # mails = User.objects.get(username=patron).email
    # print(patron,mails)
    try:
        patron = book.username
        mails = User.objects.get(username=patron).email
        send_mail(
            f'{book.serial_number}',
            f' Hi {patron.first_name} {patron.last_name}, you have returned {book.serial_number}, \n on  '
            f'{returned.return_date}. \n \n served by: {request.user.first_name}  {request.user.last_name}',
            'settings.EMAIL_HOST_USER',
            [mails],
            fail_silently=False
        )

    except:
        messages.success(request, 'Confirmation email not sent to patron')
    messages.success(request, f'{book.serial_number} has been returned')
    book.delete()
    return redirect('view_issued_books')

@staff_member_required
def viewReturnedBooks(request):
    issuedBooks = ReturnedBook.objects.all()

    return render(request, 'dashboard/returnedBooks.html',{
        'issues': issuedBooks,
    })
@staff_member_required
def exams(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            buf = form.save(commit=False)
            buf.added_by = request.user
            buf.save()
            messages.success(request, 'Exam has been added!')
            return redirect('Exams')

    form = ExamForm()
    return render(request, 'dashboard/exam.html', {'form': form })

def examsrepo(request):
    exam = Exam.objects.all()
    return render(request, 'examrepo.html', {
        'exams':exam
        })

@staff_member_required
def search_book_RUD(request):
    if request.method == 'POST':
        searched_books = request.POST['search_books'] 
        books = AddBook.objects.filter(Q(title__contains=searched_books)|Q(Author__contains=searched_books)|Q(serial_number__contains=searched_books))
        return render(request, 'dashboard/search_book_RUD.html', {'searched':searched_books,'books': books})
    elif request.method == 'GET':
        return redirect('manage')

@staff_member_required
def extendBook(request, id):
    """This deals with extending a book's due date"""
    b = IssueBook.objects.get(id=id)
    bookIssued = ExtendBookForm(instance=b)
    issuedBooks = IssueBook.objects.filter(status='active')
    if request.method == 'POST':
        new_due_date = ExtendBookForm(request.POST, instance=b)
        if new_due_date.is_valid():
            new_due_date.save()
            messages.success(request, 'Due date has been updated')
            return redirect('view_issued_books')
        else:
            messages.success(request, 'Something went wrong')


    return render(request, 'dashboard/viewIssued.html', {'extendBook': bookIssued,'issues': issuedBooks,})


def searchissuedbooks(request):
    if request.method == 'POST':
        searched_books = request.POST['search_books']
        books = IssueBook.objects.filter(Q(username__username__icontains=searched_books))
        return render(request, 'dashboard/searchIssuedBook.html', {'searched': searched_books, 'issues': books})
    elif request.method == 'GET':
        return redirect('view_issued_books')