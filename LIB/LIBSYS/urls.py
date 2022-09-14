from  django.urls import path, include
from . import views
urlpatterns = [    
    path('signup/', views.signup, name='signup'),
    path('add/', views.addBookstoShelf, name='add'),
    path('manage/',views.manageBook, name='manage'),
    path('updateBook/<str:serial_number>/', views.updateBook, name='updateBook'),
    path('delete/<str:serial_number>', views.deleteBook, name='deletebook'),
    path('blog/news', views.NewsUpdate, name='blog'),
    # path('signup/', include('django.contrib.auth.urls')),
    # path('')
]