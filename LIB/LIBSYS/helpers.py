from django.core.mail import send_mail
from django.contrib import messages
from .models import BookDetail, Book, IssueBook, Fine
from scholarly import scholarly
from .forms import IssueBookForm, BookForm, BookDetailForm, BookUpdateForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

from asgiref.sync import sync_to_async
import asyncio


def genreList():
    """This returns a set of genres in the library."""
    books = BookDetail.objects.all()
    lst = []
    for x in books:
        lst.append(x.genre)
        # print(lst)
    return set(lst)


def grab_author_details(context, author):
    try:
        search_query = scholarly.search_author(f'{author[0].Author}')
        author = scholarly.fill(next(search_query))
        strip_author = author['publications']  # seleting dict with publications
        # print(strip_author)
        counter = 0
        pub = []
        citedby = []
        num = []
        # asyncio.sleep(5)
        for k in strip_author:
            if counter < 4:
                for v in k:
                    if v == 'bib':
                        pub.append(k[v])

                    elif v == 'citedby_url':
                        citedby.append(k[v])

                    elif v == 'num_citations':
                        num.append(k[v])
            else:
                break
            counter += 1
        context['pub'] = pub
        context['citedby'] = citedby
        context['num'] = num

        print(pub)
    except:
        context['author404'] = f'Did not find books related to {author[0].author} in Google scholar'


def affiliation(request, id=False):
    """Returns a clients library branch :param:request"""
    if id:
        return request.user.profile.affiliation.id
    else:
        return request.user.profile.affiliation


def issue_book_post(request, instance=None):
    form = IssueBookForm(request.POST, instance=instance)
    if form.is_valid():
        buf = form.save(commit=False)  # hold from saving the posted info
        if buf.book_issued.book_details.copies > 0:  # TODO: copies_remaining
            # condition for checking number of copies and decrementing
            patron = form.cleaned_data['username']
            book = form.cleaned_data['book_issued'].serial_number
            is_issued = IssueBook.objects.filter(username=patron, book_issued=book).exists()
            is_overdue = Fine.objects.filter(username=patron, serial_number=book).exists()

            if not is_issued and not is_overdue:  # patron does not have the book in both fines and
                # issue book model

                patron_borrowed_books = IssueBook.objects.filter(username=patron)
                patron_over_due_book = Fine.objects.filter(username=patron)
                total_books_given = len(patron_borrowed_books) + len(patron_over_due_book)
                if total_books_given < 3:
                    book = Book.objects.filter(serial_number=form.cleaned_data['book_issued'].serial_number)
                    for x in book:
                        x.book_details.copies -= 1  # TODO: change this to copies-remaining
                        x.save()
                        # print(x.copies)
                    buf.save()
                    mails = User.objects.get(username=patron).email
                    print(mails)
                    send_mail(
                        f'{form.cleaned_data["book_issued"]}',
                        f' Hi {patron.first_name} {patron.last_name}, you have been given /'
                        f'{form.cleaned_data["book_issued"].title}, the due date is {form.cleaned_data["due_date"]}',
                        'settings.EMAIL_HOST_USER',
                        [mails],
                        fail_silently=False
                    )
                    messages.success(request,
                                     f'{form.cleaned_data["book_issued"].title} has been given to {form.cleaned_data["username"]}')
                else:
                    # TODO: Add info about the books that has borrowed, both active and over due books.
                    messages.success(request,
                                     f'{form.cleaned_data["username"]} has reached the maximum number of books '
                                     f'borrowed!')
            elif is_issued:
                messages.success(request,
                                 f'{form.cleaned_data["username"]} already has {form.cleaned_data["book_issued"].title}')
            else:
                messages.success(request,
                                 f'{form.cleaned_data["book_issued"].title} is overdue for the patron')
        else:
            messages.success(request, "No more books are available in the DB how is this possible")

        return redirect('IssueBook')


def add_update_book(
        request,
        is_update=False,
        book_instance=None,
        book_detail_instance=None,
        total_copies=0,
        serial_number=None):
    if is_update:
        bookForm = BookUpdateForm(request.POST, instance=book_instance)
    else:
        bookForm = BookForm(request.POST, instance=book_instance)
    bookDetailForm = BookDetailForm(request.POST, request.FILES, instance=book_detail_instance)

    if bookDetailForm.is_valid() and bookForm.is_valid():
        bookFormbuffer = bookForm.save(commit=False)
        bookFormbuffer.library_id = affiliation(request, id=True)
        buffer = bookDetailForm.save(commit=False)
        if is_update:
            if buffer.copies > total_copies:
                copies_added = buffer.copies - total_copies
                buffer.copies_remaining += copies_added  # add the difference to the copies remaining in repo
        else:
            buffer.copies_remaining = buffer.copies
        buffer.save()
        bookFormbuffer.book_details_id = buffer.id
        bookFormbuffer.save()

        if is_update:
            messages.success(request, f"{bookForm.cleaned_data['title']} has been updated!")
            return redirect("updateBook", serial_number)
        else:
            messages.success(request, "Book added successfully")
            return redirect("add")
    else:
        messages.success(request, "Something went wrong")
        if is_update:
            return redirect("updateBook", serial_number)
        else:
            return redirect("add")
