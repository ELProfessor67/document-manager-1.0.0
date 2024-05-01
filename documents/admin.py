from django.contrib import admin
from .models import Documents,Role, UsersDocuments

admin.site.register(Documents)
admin.site.register(Role)
admin.site.register(UsersDocuments)
