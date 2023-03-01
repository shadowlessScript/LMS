from  django.urls import path, include
from . import views
urlpatterns = [   
    path('',views.index, name="home"),
    path('home_user_view/',views.indexuserview, name="home_user_view"),
    path('add/', views.addBookstoShelf, name='add'),
    path('manage/',views.manageBook, name='manage'),
    path('updateBook/<str:serial_number>/', views.updateBook, name='updateBook'),
    path('delete/<str:serial_number>/', views.deleteBook, name='deletebook'),
    path('delete_Confirm/<str:serial_number>/', views.deleteBookConfirmation, name='deletebook_confirm'),
    path('blog/news/', views.PostNews, name='blog'),
    path('books/',views.ListOfBooks, name="books"),
    path('view/<str:serial_number>/', views.bookView, name='bookview'),
    path('update_news/<int:id>/',views.NewsUpdate, name='update_news'),
    path('filter_view/<str:genre>/', views.Filter, name='filtered_view'),
    path('error404',views.Notfound, name='404'),
    path('results/', views.search_book, name='search_books'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:id>/<str:username>/<str:serial_number>', views.issuebookrequest, name='issuebookrequest'),
    path('issuebook/', views.issueBook, name='IssueBook'),
    path('view_issued_books/', views.viewIssuedBooks, name='view_issued_books'),
    path('overdue_books/', views.overdue, name='overdue'),
    path('bookacquire/', views.bookAcquisitionRequest, name='bookacquire'),
    path('getthisbook/', views.getthisbook, name='getthisbook'),
    path('status_update/<int:id>', views.questCompleted, name='status_update'),
    path('bookreturned/<int:id>', views.returnedBook, name='bookreturned'),
    path('viewreturnedbooks/', views.viewReturnedBooks, name='viewreturnedbooks'),
]