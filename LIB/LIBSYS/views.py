from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from .forms import AddBookForm, NewsForm, IssueBookForm, BookAcquisitionRequestForm, ExamForm, ExtendBookForm, RatingForm, BookReviewForm
from .models import AddBook,New, Booking, IssueBook, BookAcquisitionRequest, ReturnedBook, Exam, Fine, Rating, Bookmark, History, BookReview
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime, timedelta
from django.db.models import Q
from django_daraja.mpesa.core import MpesaClient
# from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from .recommenders import user_user_collab_filtering, content_based_recommender_sys
from .helpers import genreList, grab_author_details
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
library_of_congress = {
    'A': 'General Works (encyclopedias, dictionaries, etc.)',
    'B': 'Philosophy',
    'BF': 'Psychology',
    'BL-BX': 'Religion',
    'C': 'Genealogy, Biography',
    'D': 'History-General & Eastern Hemispheres',
    'E-F': 'History--Americas',
    'G': 'Geography, Anthropology, Recreation',
    'HB-HJ': 'Business & Economics',
    'HM-HQ': "Sociology, Family, Women's Studies",
    'J': 'Political Sciences',
    'K': 'Law',
    'L': 'Education',
    'M': 'Music and books on Music',
    'N': 'Fine Arts',
    'P': 'Language & Literature',
    'Q-QD': 'Math, Physics, Chemistry',
    'QE': 'Geology',
    'QH-QK': 'Biology, Botany',
    'QL-QR': 'Zoology, Physiology, Microbiology',
    'TA-TK': 'Engineering, Computing',
    'U': 'Military Science',
    'V': 'Naval Science',
    'Z': 'History of Books & Printing, Library Science, Bibliography'
}
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
    context = {
    'storys': posts,    
    }
   
    if not request.user.is_anonymous:        
        patron_history = History.objects.filter(username=request.user).order_by('-checked_at')
        context['history'] = patron_history[:5]

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
    
    recommended_list = user_user_collab_filtering(request)
    # print(recommended_list)
    if recommended_list:
        print('tooo')
        return render(request, "shelfs/book.html", {
            'Books': b,
            'Genres': genreList(),
            'recommendedbooks': recommended_list,
        })
        
    else:
        r = content_based_recommender_sys(request)
        content_based_list = []
        if r:
            content_based_list = [AddBook.objects.filter(title=title) for title in r[1]]
        
        print(content_based_list)
        if content_based_list:
            return render(request, "shelfs/book.html", {
                'Books': b,
                'Genres': genreList(),
                'recommendedbooks': content_based_list,
                'rectitle': r[0],
            })
        else:
            
            return render(request, "shelfs/book.html", {
                'Books': b,
                'Genres': genreList(),
        })


# @sync_to_async
@login_required
# @async_to_sync
def bookView(request, serial_number):
    from statistics import mean
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
    if Rating.objects.filter(serial_number=serial_number).exists():
        book_rating = Rating.objects.filter(serial_number_id=serial_number)
        avg_rating = mean([i.rate for i in book_rating])
    else:
        avg_rating = 0
    patron_bookmark = Bookmark.objects.filter(username=request.user, book=serial_number)
    reviews = BookReview.objects.filter(book=serial_number)
    has_history = History.objects.filter(username=request.user, serial_number=serial_number).exists()
    if not has_history:
        create_history = History.objects.create(username=request.user, serial_number_id=serial_number)
        create_history.save()
    else:
        for i in History.objects.filter(username=request.user, serial_number=serial_number):
            i.checked_at = datetime.now()
            i.save()
    # print(whichbook[0].Author)
    context = {
        'Book': whichbook, 
        'bookmark': patron_bookmark, 
        'reviews': reviews, 
        "serial":serial_number,
        "avg_rate": avg_rating
        }
    # task = asyncio.ensure_future( grab_author_details(context=context, author=whichbook))
    grab_author_details(context=context, author=whichbook)
    return render(request, 'shelfs/bookview.html', context)
    # return HttpResponse('Yoo')


# creating a filter functionality
@login_required
def Filter(request, genre):
    book_filtered = AddBook.objects.filter(genre = genre)    
    context = {
        'Book': book_filtered,
        'Genres': genreList(),
    }
    return render(request, 'shelfs/filter.html', context)
# end of filter function

@login_required
def search_book(request):
    if request.method == 'POST':
        searched_books = request.POST['searched_books']  
        books = AddBook.objects.filter(Q(title__contains=searched_books)|Q(Author__contains=searched_books)|Q(serial_number__contains=searched_books)) 
        if books == []:
            print(books)
            # BY: BEN MUNYASIA BCSC01/0018/2018
     
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
    print(IssueBook.objects.filter(issuedate__range=(end_date, start_date)).count())
    return render(request, 'dashboard/dashboard.html', {
        'counter':request_counter,
        'number_of_books': number_of_books,
        'fines': Fine.objects.count(),
        'BAR': BookAcquisitionRequest.objects.filter(status='Pending').count(), # BAR --> BookAcquisitionRequest
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
                # condition for checking number of copies and decrementing. # BY: BEN MUNYASIA BCSC01/0018/2018

                
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
            if buf.isbn.copies > 0:
                # condition for checking number of copies and decrementing
                patron = form.cleaned_data['username']
                book = form.cleaned_data['isbn'].serial_number
                check_patron = IssueBook.objects.filter(username=patron, isbn=book).exists()
                if not check_patron:
                    patron_borrowed_books = IssueBook.objects.filter(username=patron)
                    
                    if len(patron_borrowed_books) < 3: 
                        book = AddBook.objects.filter(serial_number=form.cleaned_data['isbn'].serial_number)
                        for x in book:
                            x.copies -=  1
                            x.save()
                            #print(x.copies)
                        buf.save()                
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
                        messages.success(request, f'{form.cleaned_data["username"]} has reached the maximum number of books borrowed!')
                else:
                    messages.success(request, f'{form.cleaned_data["username"]} already has {form.cleaned_data["isbn"].title}')
            else:
                messages.success(request, "No more books are available in the DB how is this possible")
            
            
            return redirect('IssueBook')
    else:
        # issueset = inlineformset_factory(AddBook, IssueBook, fields=('__all__'))
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
       'issues': b, # BY: BEN MUNYASIA BCSC01/0018/2018

       }
   return render(request, 'dashboard/viewIssued.html', context)

@staff_member_required
def overdue(request):
   issuedBooks = Fine.objects.all()
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
    hydrate = AddBook.objects.get(pk=book.isbn.serial_number)
    hydrate.copies += 1
    hydrate.save()
    returned = ReturnedBook(username=book.username, serial_number=book.isbn)
    returned.save()
    # patron = book.username
    # mails = User.objects.get(username=patron).email
    # print(patron,mails)
    try:
        patron = book.username
        mails = User.objects.get(username=patron).email
        send_mail(
            f'{book.isbn.title}',
            f' Hi {patron.first_name} {patron.last_name}, you have returned {book.isbn.title}, \n on  '
            f'{returned.return_date}. \n \n served by: {request.user.first_name}  {request.user.last_name}',
            'settings.EMAIL_HOST_USER',
            [mails],
            fail_silently=False
        )

    except:
        messages.success(request, 'Confirmation email not sent to patron')
    messages.success(request, f'{book.isbn} has been returned')
    book.delete()
    return redirect('view_issued_books')

@staff_member_required
def viewReturnedBooks(request):
    issuedBooks = ReturnedBook.objects.all().order_by('-return_date') # starts with the latest book returned

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

@staff_member_required
def searchissuedbooks(request):
    if request.method == 'POST':
        searched_books = request.POST['search_books']
        books = IssueBook.objects.filter(Q(username__username__icontains=searched_books))
        return render(request, 'dashboard/searchIssuedBook.html', {'searched': searched_books, 'issues': books})
    elif request.method == 'GET':
        return redirect('view_issued_books')

@login_required
def rate(request, username, serial_number):
    # populate like the bookview page the patron was in
    whichbook = AddBook.objects.filter(serial_number=serial_number)
    if request.method == 'POST':
        try:
            t = Rating.objects.get(serial_number=serial_number, username=request.user.id)
            # update the existing rating of the patron
            form = RatingForm(request.POST, instance=t)
            if form.is_valid():
                buf = form.save(commit=False)
                buf.username = request.user
                buf.serial_number_id = serial_number
                buf.save()
                return redirect('bookview', serial_number)
        except:
            form = RatingForm(request.POST)
            if form.is_valid():
                buf = form.save(commit=False)
                buf.username = request.user
                buf.serial_number_id = serial_number
                buf.save()
                return redirect('bookview', serial_number)
    try:
        # will be used check if patron has already rated this book
        t = Rating.objects.get(serial_number=serial_number, username=request.user.id)
        form = RatingForm(instance=t)
        return render(request, 'shelfs/bookview.html', {'form': form, 'Book': whichbook})
    except:
        # first time rating it
        return render(request, 'shelfs/bookview.html', {'form': RatingForm(), 'Book': whichbook})

@login_required
def patronpage(request):
    request_status = BookAcquisitionRequest.objects.filter(requester=request.user)
    books_borrowed = IssueBook.objects.filter(username=request.user)
    returned = ReturnedBook.objects.filter(username=request.user)
    overdueBooks = Fine.objects.filter(username=request.user)
    patron_bookmark = Bookmark.objects.filter(username=request.user)
    p = Paginator(patron_bookmark.order_by('book'), 4)
    page = request.GET.get('page')
    b = p.get_page(page)
    for x in patron_bookmark:
        print(x.book.Cover_image)
    return render(request, 'patronpage.html', {
        'request_status': request_status,
        'borrowed': books_borrowed,
        'returned': returned,
        'overdueBooks': overdueBooks,
        'bookmark': b,
    })


#     cl = MpesaClient()
#     # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
#     phone_number = U
#     amount = 1
#     account_reference = 'reference'
#     transaction_desc = 'Description'
#     callback_url = 'https://darajambili.herokuapp.com/express-payment'
#     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#     return HttpResponse(response)
#
#
# def stk_push_callback(request):
#     data = request.body
#
#     return HttpResponse("STK Push in Django👋")

@staff_member_required
def finepaid(request, id):
    fine = Fine.objects.get(id=id)
    fine.status = 'Paid'
    fine.save()
    return redirect('overdue')

@staff_member_required
def returnfinedbook(request, id):
    fined_book = Fine.objects.get(id=id)
    patron_mail = fined_book.username.email
    # check if fine has been paid
    if fined_book.status == 'Paid':
        returned = ReturnedBook(username=fined_book.username, serial_number=fined_book.serial_number)
        returned.save()
        print(fined_book)
        messages.success(request, f'{fined_book.username.first_name} {fined_book.username.last_name} has returned their book.')
        fined_book.delete()
        send_mail(
            f'{fined_book.serial_number.title}',
            f' Hi {fined_book.username.first_name} {fined_book.username.last_name}, you have returned your over due book: {fined_book.serial_number.title}, \n on  '
            f'{datetime.today()}. \n \n served by: {request.user.first_name}  {request.user.last_name}',
            'settings.EMAIL_HOST_USER',
            [patron_mail],
            fail_silently=False
        )
    else:
        print(patron_mail)
        messages.success(request, f'{fined_book.username.first_name} {fined_book.username.last_name} has not paid their fine.')
    return redirect('overdue')

@login_required
def bookmark(request, book):
    book1 = AddBook.objects.get(serial_number=book)
    patron_bookmark = Bookmark(username=request.user, book=book1)
    if Bookmark.objects.filter(username=request.user, book=book1).exists():
        messages.success(request, f'You have already bookmarked {patron_bookmark.book.title}')
        return redirect('bookview', book)
    else:
        patron_bookmark.save()
        return redirect('bookview', book)

@login_required
def removebookmark(request, id):
    book = Bookmark.objects.get(id=id)
    serial_number = book.book.serial_number
    print(f'/removebookmark/{book.id}/')
    # if _path == f'/mypage/':
    if request.path == f"/removebookmark/{book.id}/":  
        messages.success(request, f'{book.book.title} has been removed from your bookmark list')
        book.delete()
        return redirect('mypage')
    elif request.path == f"/removebmk/{book.id}/":
        messages.success(request, f'{book.book.title} has been removed from your bookmark list')
        book.delete()
        return redirect('bookview', serial_number)
    # return redirect('mypage')

@login_required
def reviewbook(request, serial_number):
    # populate like the bookview page the patron was in
    whichbook = AddBook.objects.filter(serial_number=serial_number)
    if request.method == 'POST':
        try:
            t = BookReview.objects.get(book=serial_number, username=request.user.id)
            # update the existing rating of the patron
            form = BookReviewForm(request.POST, instance=t)
            if form.is_valid():
                buf = form.save(commit=False)
                buf.username = request.user
                buf.book_id = serial_number
                buf.save()
                return redirect('bookview', serial_number)
        except:
            form = BookReviewForm(request.POST)
            if form.is_valid():
                buf = form.save(commit=False)
                buf.username = request.user
                buf.book_id = serial_number
                buf.save()
                return redirect('bookview', serial_number)
    try:
        # will be used check if patron has already reviewed this book
        t = BookReview.objects.get(book=serial_number, username=request.user.id)
        form = BookReviewForm(instance=t)
        return render(request, 'shelfs/bookview.html', {'reviewform': form, 'Book': whichbook})
    except:
        # first time reviewing/commenting it
        return render(request, 'shelfs/bookview.html', {'reviewform': BookReviewForm(), 'Book': whichbook})
    
@staff_member_required
def examrepomanage(request):
    exams = Exam.objects.all()
    print(exams)
    return render(request, 'dashboard/manageexamrepo.html', {'exams': exams})

@staff_member_required
def updateexam(request,id):
    exams = Exam.objects.get(id=id)
    if request.method == 'POST':
        exams = Exam.objects.get(id=id)
        form = ExamForm(request.POST, request.FILES, instance=exams)
        if form.is_valid():
            buf = form.save(commit=False)
            buf.added_by = request.user
            buf.save()
            messages.success(request, 'Exam has been updated!')
            return redirect('manageexamrepo')

    form = ExamForm(instance=exams)
    
    return render(request, 'dashboard/updateexam.html', {'form': form })
@staff_member_required
def deleteexam(request,id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    messages.success(request, 'Exam has been deleted!')
    return redirect('manageexamrepo')
@login_required
def deletebookquest(request, id):
    quest = BookAcquisitionRequest.objects.get(id=id)
    quest.delete()
    messages.success(request, 'Book request deleted!')
    return redirect('mypage')

@login_required
def filter_by_author(request, author):
    get_author_book = AddBook.objects.filter(Author=author) 
    return render(request, 'shelfs/filter.html', {
        'Genres': genreList()
        ,'Book': get_author_book})

@login_required
def books_location(request):    

    locations = AddBook.objects.all()
    return render(request, 'location.html', {'locations':locations,
                                              'library_of_congress':library_of_congress
                                              })

@login_required
def filterloc(request,sym):
    get_book_located = AddBook.objects.filter(call_number__istartswith=sym)
    return render(request, 'location.html', {'locations':get_book_located,
                                              'library_of_congress':library_of_congress
                                              })
   

