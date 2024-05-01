
from django.contrib import admin
from django.urls import path, include
from .views import upoadDocument,getOneDoucment

urlpatterns = [
    path('documents-uploads',upoadDocument,name="default document"),
    path('upoload-document/<int:document_id>',getOneDoucment,name="upload lists"),
]
