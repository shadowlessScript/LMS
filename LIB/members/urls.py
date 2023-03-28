from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
   path('login_user/', views.login_user, name='login'),
   path('login_out/', views.logout_user, name='logout'),
   path('register_user/', views.register_user, name='register'),
   path('profile/', views.profile, name='profile'),
   path('password/', auth_view.PasswordChangeView.as_view(template_name="authenticate/change-password.html")),
   path('payfine/', views.payfine, name='payfine'),
   # path('mpesa/stk_push/', views.stk_push_callback, name='stk_push_callback'),
]