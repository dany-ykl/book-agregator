from django.urls import path
from . import views

app_name = 'agregator'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-view'),
    path('search/', views.BookView.as_view(), name='get-book')
]