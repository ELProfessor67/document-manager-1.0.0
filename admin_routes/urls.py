
from django.contrib import admin
from django.urls import path, include
from .views import admin_dashboard, add_docuemnt, add_role, all_users, user_details, sendmail, editDocument

urlpatterns = [
    path('dashboard',admin_dashboard,name='admin dashboard'),
    path('dashboard/add-document',add_docuemnt,name='add document'),
    path('dashboard/add-role',add_role,name='add role'),
    path('dashboard/all-users',all_users,name='all users'),
    path('dashboard/user/<int:id>/', user_details, name='user_details'),
    path('dashbaord/edit/<int:id>', editDocument, name='edit document'),
    path('send-mail/<int:document_id>/<int:user_id>/',sendmail,name="upload lists"),
   
]
