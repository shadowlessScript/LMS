from django.contrib import admin
from .models import AddBook, New,BorrowBook
# Register your models here.
admin.site.register(BorrowBook)
admin.site.register(New)
admin.site.register(AddBook)