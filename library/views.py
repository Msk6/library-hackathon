from django.shortcuts import render, redirect
from .forms import SigninForm, SignupForm, AddBookForm
from django.contrib.auth import login, authenticate, logout
from .models import Librarian, Book
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def signin(request):
    form = SigninForm() 
    if request.method == 'POST':
        form = SigninForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return render(request, 'test.html')
              
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def create_membership(request):
    form = SignupForm()
    # permision
    '''user_obj = Librarian.objects.filter(user=request.user)
    if not (user_obj == request.user):
        return redirect('signin')'''

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hashing before saving
            user.set_password(user.password)
            user.save()
            return redirect("book-list")
    
    context = {
        "form":form,
    }
    return render(request, 'create_membership.html', context)

def books_list(request):
    books = Book.objects.all()

    query = request.GET.get('book')
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query)|
            Q(ISBN__icontains=query)|
            Q(author__icontains=query)
        ).distinct()
    context = {
        'books': books
    }

    return render(request, 'book_list.html', context)


def add_book(request):
    # permision
    '''user_obj = Librarian.objects.filter(user=request.user)
    if user_obj != request.user:
        return redirect('signin')'''

    form = AddBookForm()
    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added book')
            return redirect('add-book')
    context = {
        "form":form,
    }
    return render(request, 'add_book.html', context)


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    logs = book.logs.all()
    context = {
        'book': book,
        'logs': logs,
    }
    return render(request, 'book_detail.html', context)

