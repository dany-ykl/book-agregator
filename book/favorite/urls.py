from django.urls import path
from . import views

app_name = 'favorite'

urlpatterns = [
    path('', views.BookView.as_view(), name='book-list')
]