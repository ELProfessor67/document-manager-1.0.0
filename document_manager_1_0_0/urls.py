
from django.contrib import admin
from django.urls import path, include
from .views import register, user_login, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register,name='register'),
    path('',user_login,name='login'),
    path('',include('documents.urls')),
    path('',include('admin_routes.urls')),
    path('logout/', logout_view, name='logout'),
]
