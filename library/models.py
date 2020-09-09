from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    # Details
    name = models.CharField(max_length=550)
    author = models.CharField(max_length=250)
    year_of_release = models.IntegerField()
    ISBN = models.IntegerField(unique=True,)
    genre = models.TextField(max_length=650)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    # logs
    availability = models.BooleanField(default=False)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='logs')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='logs')