from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from.forms import LoginForm
app_name = 'auth_task'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name = 'auth_task/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'auth_task/logout.html'), name='logout'),
]