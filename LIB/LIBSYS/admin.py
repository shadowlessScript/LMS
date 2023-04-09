from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import AddBook, New, Fine, Booking, IssueBook, BookAcquisitionRequest, ReturnedBook, Exam, Rating, Bookmark, History, BookReview
# Register your models here.

admin.site.register(New)
admin.site.register(AddBook)
# admin.site.unregister(Fine)
admin.site.register(Fine)
admin.site.register(Booking)
admin.site.register(IssueBook)
admin.site.register(BookAcquisitionRequest)
admin.site.register(ReturnedBook)
admin.site.register(Exam)
admin.site.register(Rating)
admin.site.register(Bookmark)
admin.site.register(History)
admin.site.register(BookReview)