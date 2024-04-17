from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from auth_task.views import MyPasswordResetView, MyPasswordResetConfirmView
from . import views
from.forms import LoginForm
app_name = 'auth_task'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name = 'auth_task/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'auth_task/logout.html'), name='logout'),
    path('password_reset/', MyPasswordResetView.as_view(template_name = 'auth_task/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'auth_task/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(template_name = 'auth_task/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/Mw/set-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'auth_task/password_reset_complete.html'), name='password_reset_complete'),
]