
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'quotes_task'
urlpatterns = [
    path('', views.index, name='home'),
    
    path('author/<int:author_id>/', views.author_show, name='author_show'),
    path('addquote/', views.add_quote, name='add_quote'),
    path('addauthor/', views.add_author, name='add_author'),
]
