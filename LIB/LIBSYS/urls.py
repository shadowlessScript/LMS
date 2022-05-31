from  django.urls import path, include
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('add/', views.addBookstoShelf, name='add')
    # path('signup/', include('django.contrib.auth.urls')),
    # path('')
]