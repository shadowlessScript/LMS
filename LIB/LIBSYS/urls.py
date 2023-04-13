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
    path('booking/<int:id>/<str:isbn>', views.issuebookrequest, name='issuebookrequest'),
    path('issuebook/', views.issueBook, name='IssueBook'),
    path('view_issued_books/', views.viewIssuedBooks, name='view_issued_books'),
    path('overdue_books/', views.overdue, name='overdue'),
    path('bookacquire/', views.bookAcquisitionRequest, name='bookacquire'),
    path('getthisbook/', views.getthisbook, name='getthisbook'),
    path('status_update/<int:id>', views.questCompleted, name='status_update'),
    path('bookreturned/<int:id>', views.returnedBook, name='bookreturned'),
    path('viewreturnedbooks/', views.viewReturnedBooks, name='viewreturnedbooks'),
    path('addexams/', views.exams, name="Exams"),
    path('examsrepo/', views.examsrepo, name='examrepo'),
    path('search_book_RUD', views.search_book_RUD, name="search_book_RUD"),
    path('extendBook/<int:id>', views.extendBook, name='extendBook'),
    path('searchissuedbook/', views.searchissuedbooks, name='searchissuedbook'),
    path('rate/<str:username>/<str:serial_number>/', views.rate, name='rate'),
    path('mypage/', views.patronpage, name='mypage'),
    path('finepaid/<int:id>/', views.finepaid, name='finepaid'),
    path('bookmark/<str:book>/', views.bookmark, name='bookmark'),
    path('finedbookreturned/<int:id>/', views.returnfinedbook, name='finedbookreturned'),
    path('removebookmark/<int:id>/', views.removebookmark, name='removebmk'),
    path('removebmk/<int:id>/', views.removebookmark, name='removebmrk'),
    path('reviewbook/<str:serial_number>/', views.reviewbook, name="reviewbook"),
    path('manageexamrepo', views.examrepomanage, name='manageexamrepo'),
    path('updateexam/<int:id>', views.updateexam, name='updateexam'),
    path('deleteexam/<int:id>', views.deleteexam, name='deleteexam'),
    path('deletebookquest/<int:id>', views.deletebookquest, name='deletequest')
    # mpesa push
    # path('mpesa/stk_push/', views.stk_push_callback, name='stk_push_callback'),

]