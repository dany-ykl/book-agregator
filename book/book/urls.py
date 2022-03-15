from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agregator.urls')),
    path('accounts/', include('accounts.urls')),
    path('favorite/', include('favorite.urls')),
]
