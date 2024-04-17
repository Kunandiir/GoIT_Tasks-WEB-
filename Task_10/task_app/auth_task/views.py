from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import RegisterForm


class MyPasswordResetView(auth_views.PasswordResetView):
    success_url = "done"


class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = "complete"


class RegisterView(View):
    template_name = 'auth_task/register.html'
    form_class = RegisterForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(to='quotes_task:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, message=f'Congrats {username}. Account sucesfuly created')
            return redirect(to='auth_task:login')
        return render(request, self.template_name, context= {'form': form})