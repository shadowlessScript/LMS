from  django.urls import path, include
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('add/', views.addBookstoShelf, name='add'),
    path('manage/',views.manageBook),
    path('updateBook/<serial_number>/', views.updateBook, name='updateBook'),
    # path('signup/', include('django.contrib.auth.urls')),
    # path('')
]