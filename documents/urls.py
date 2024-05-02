
from django.contrib import admin
from django.urls import path, include
from .views import upoadDocument,getOneDoucment,ListDocument

urlpatterns = [
    path('documents-uploads',upoadDocument,name="default document"),
    path('upoload-document/<int:document_id>',getOneDoucment,name="upload lists"),
    path('documents-lists/',ListDocument,name="upload lists"),
]
