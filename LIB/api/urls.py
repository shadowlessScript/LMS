
from django.urls import path, include
from .views import getData, mobileLogin, mobileLogOut, getBookData, getBookDetails

urlpatterns = [
    path("", getData, name="api_endpoint"),
    path("login/", mobileLogin, name="login_endpoint"),
    path("logout/", mobileLogOut, name="logout_endpoint"),
    path("booksrepo/",getBookData, name="bookRepo_endpoint"),
    path("bookdetails/<str:serial_number/", getBookDetails, name="bookDetails_endpoint"),
    ]

