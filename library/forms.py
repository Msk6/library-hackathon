from django import forms
from django.contrib.auth.models import User
from .models import Book

class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'