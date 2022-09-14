from django.contrib import admin
from .models import signupForm, AddBook, New
# Register your models here.
admin.site.register(signupForm)
admin.site.register(New)
admin.site.register(AddBook)