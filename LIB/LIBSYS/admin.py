from django.contrib import admin
from .models import AddBook, New,BorrowBook, Fine, Booking, IssueBook, BookAcquisitionRequest, ReturnedBook
# Register your models here.
admin.site.register(BorrowBook)
admin.site.register(New)
admin.site.register(AddBook)
admin.site.register(Fine)
admin.site.register(Booking)
admin.site.register(IssueBook)
admin.site.register(BookAcquisitionRequest)
admin.site.register(ReturnedBook)
