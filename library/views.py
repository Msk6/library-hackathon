from django.shortcuts import render, redirect
from .forms import SigninForm, SignupForm, AddBookForm, AddLog
from django.contrib.auth import login, authenticate, logout
from .models import Librarian, Book
from django.contrib import messages
from django.db.models import Q
import datetime

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
                return redirect('book-list')
              
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")


def create_membership(request):
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)
    except:
       return redirect('signin')
    
    form = SignupForm()
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
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)
        is_lib = True
    except:
        is_lib = False

    books = Book.objects.all()
    # serach
    query = request.GET.get('book')

    if query:
        books = Book.objects.filter(
            Q(name__icontains=query)|
            Q(ISBN__icontains=query)|
            Q(author__icontains=query)
        ).distinct()

    context = {
        'books': books,
        'is_lib': is_lib,
    }

    return render(request, 'book_list.html', context)


def add_book(request):
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)
    except:
        return redirect('signin')
    

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
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)
        is_lib = True
    except:
        is_lib = False
    
    book = Book.objects.get(id=book_id)
    logs = book.logs.all()
    try:
        last_log = book.logs.get(return_date__isnull=True)
        available = False
    except:
        available = True

    context = {
        'book': book,
        'logs': logs,
        'available': available,
        'is_lib': is_lib,

    }
    return render(request, 'book_detail.html', context)

# All books in the log have a return_date except borrowed books have null
def add_log(request, book_id):
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)    
    except:
        return redirect('signin')
        

    book = Book.objects.get(id=book_id)
    try:
        last_log = book.logs.get(return_date__isnull=True)
        messages.success(request, 'The book is unavailable')
        return redirect('book-list')

    except:
        form = AddLog()
        if request.method == "POST":
            form = AddLog(request.POST)
            if form.is_valid():
                log_obj = form.save(commit=False)
                log_obj.set_book(book)
                log_obj.save()
                messages.success(request, 'Book is borrow')
                return redirect('book-list')

        context = {
            'form': form,
            'book': book,
        }

        return render(request, 'add_log.html', context)


def return_book(request, book_id):
    # permision
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user)    
    except:
        return redirect('signin')

    book = Book.objects.get(id=book_id)
    try:
        last_log = book.logs.get(return_date__isnull=True)
        if not last_log.availability:
            last_log.set_availability(True)
            last_log.set_return_date(datetime.datetime.now())
            last_log.save()
            messages.success(request, 'Cngrats the book returned')
            return redirect('book-list')
    except:
        messages.success(request, 'The book is availlable')
        return redirect('book-list')

def history(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user) 
        return redirect('signin')   

    except:
        user_obj = request.user
        user_logs = user_obj.logs.all()
        #user_logs = Log.objects.filter(user=request.user)
        context = {
            'user_logs': user_logs,
        }

        return render(request, 'history.html', context)


def reversed_books(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user) 
        return redirect('signin') 
    except: 
        user_obj = request.user
        user_logs = user_obj.logs.filter(return_date__isnull=True)
        #user_logs = Log.objects.filter(user=request.user)
        context = {
            'user_logs': user_logs,
        }

        return render(request, 'reversed_books.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user_obj = Librarian.objects.get(user=request.user) 
        return redirect('signin') 
    except: 
        context = {
            'user': request.user
        }

        return render(request, 'personal_info.html', context)

    




