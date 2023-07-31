
from django.urls import path, include
from .views import getData, mobile_login, mobileLogOut, getBookData, getBookDetails, get_search_results

urlpatterns = [
    path("", getData, name="api_endpoint"),
    path("login/", mobile_login, name="login_endpoint"),
    path("logout/", mobileLogOut, name="logout_endpoint"),
    path("booksrepo/",getBookData, name="bookRepo_endpoint"),
    path("bookdetails/<str:serial_number>/", getBookDetails, name="bookDetails_endpoint"),
    path("search/<str:search_query>/", get_search_results, name="searchResult_endpoint"),
    ]

