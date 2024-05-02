from django.db import models
import os
from django.contrib.auth.models import User

def custom_upload_to(instance, filename):
    # Get the file extension
    _, ext = os.path.splitext(filename)
    # Construct the final filename
    final_filename = f'{instance.name}{ext}'
    # Define the path where you want to save the file
    return os.path.join('static', 'forms', final_filename)

def custom_document_upload_to(instance, filename):
    # Get the file extension
    _, ext = os.path.splitext(filename)
    # Construct the final filename
    final_filename = f'{instance.document.name}{ext}'
    # Define the path where you want to save the file
    return os.path.join('static', 'users',instance.user.username, final_filename)


class Documents(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    files = models.FileField(upload_to=custom_upload_to, null=True, blank=True)
    is_have_form = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else 'Unnamed'
    


class UsersDocuments(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)   
    files = models.FileField(upload_to=custom_document_upload_to, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=None)
    is_approved = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.document.name}-{self.user.username}" if self.document.name else 'Unnamed'




class Role(models.Model):
    name = models.CharField(max_length=100)
    documents = models.ManyToManyField(Documents)

    def __str__(self):
        return self.name
    


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username