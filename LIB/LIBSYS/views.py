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
from scholarly import scholarly, ProxyGenerator
from django_daraja.mpesa.core import MpesaClient
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
    # Data processing
    import pandas as pd
    import numpy as np
    import scipy.stats
    from sklearn.metrics.pairwise import cosine_similarity

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
    if Rating.objects.all().count() != 0:
        """ Recommender system algo """

        # Convert the data model to a dataframe
        ratings = pd.DataFrame(list(Rating.objects.all().values()))
        # renaming the columns of the ratings model to match with the key columns of the Addbook model
        ratings.rename(columns={"username_id":"username", "serial_number_id":"serial_number"},inplace=True)
        books_repo = pd.DataFrame(list(AddBook.objects.all().values()))
        df = pd.merge(ratings, books_repo, on='serial_number', how='inner')
        agg_ratings = df.groupby('serial_number').agg(mean_rating = ('rate', 'mean'),
                                                    number_of_rating=('rate', 'count')).reset_index()
        matrix = df.pivot_table(index='username', columns='serial_number', values='rate')
        # Normalize user-item matrix
        matrix_norm = matrix.subtract(matrix.mean(axis=1), axis='rows')
        # User similarity matrix using Pearson correlation
        user_similarity = matrix_norm.T.corr(method='kendall', min_periods=1)
        print(user_similarity)
        # Pick a user ID
        # check if user has rated any book
        print('Hi', request.user)
        print(Rating.objects.filter(username_id=request.user.id).exists())
        if Rating.objects.filter(username_id=request.user.id).exists():
            picked_userid = request.user.id

            # Remove picked user ID from the candidate list
            user_similarity.drop(index=picked_userid, inplace=True)

            # Take a look at the data
            print(picked_userid)
            # Number of similar users
            n = 10

            # User similarity threashold
            user_similarity_threshold = 0.0

            # Get top n similar users
            similar_users = user_similarity[user_similarity[picked_userid] >= user_similarity_threshold][
                                picked_userid].sort_values(ascending=False)[:n]
            # Books that the target user has read
            picked_userid_read = matrix_norm[matrix_norm.index == picked_userid].dropna(axis=1, how='all')

            # Print out top n similar users
            # print(f'The similar users for user {picked_userid} are', similar_users)
            # Books that similar users read. Remove books that none of the similar users have read
            similar_user_books = matrix_norm[matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
            # Remove the read books from the book lists
            similar_user_books.drop(picked_userid_read.columns, axis=1, inplace=True, errors='ignore')
            # A dictionary to store item scores
            item_score = {}

            # Loop through items
            for i in similar_user_books.columns:
                # Get the ratings for book i
                book_rating = similar_user_books[i]
                # Create a variable to store the score
                total = 0
                # Create a variable to store the number of scores
                count = 0
                # Loop through similar users
                for u in similar_users.index:
                    # If the book has rating
                    if pd.isna(book_rating[u]) == False:
                        # Score is the sum of user similarity score multiply by the book rating
                        score = similar_users[u] * book_rating[u]
                        # Add the score to the total score for the book so far
                        total += score
                        # Add 1 to the count
                        count += 1
                # Get the average score for the item
                item_score[i] = total / count

            # Convert dictionary to pandas dataframe
            item_score = pd.DataFrame(item_score.items(), columns=['book', 'book_score'])

            # Sort the books by score
            ranked_item_score = item_score.sort_values(by='book_score', ascending=False)

            # Select top m books
            m = 10
            ranked_item_score.head(m)
            ranked_item_score.drop(['book_score'],axis=1, inplace=True, errors='ignore')
            recommended_list = []
            for k in ranked_item_score['book']:
                if k != 1:
                    recommended_list.append(AddBook.objects.filter(serial_number=k))
            print(recommended_list)
            return render(request, "shelfs/book.html", {
                'Books': b,
                'Genres': genreList(genre),
                'recommendedbooks': recommended_list,
            })
        else:
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
    context = {'Book': whichbook, 'bookmark': patron_bookmark, 'reviews': reviews}
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
    # check if fine has been paid
    if fined_book.status == 'Paid':
        returned = ReturnedBook(username=fined_book.username, serial_number=fined_book.serial_number)
        returned.save()
        print(fined_book)
        messages.success(request, f'{fined_book.username.first_name} {fined_book.username.last_name} has returned their book.')
        fined_book.delete()

    else:
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