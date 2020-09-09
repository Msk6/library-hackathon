from django.contrib import admin
from .models import Librarian, Book, Log
# Register your models here.

admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(Log)