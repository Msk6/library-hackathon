from django.shortcuts import render, redirect
from .forms import SigninForm, SignupForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
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

def create_membership(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Hashing before saving
            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("book-list")
    context = {
        "form":form,
    }
    return render(request, 'create_membership.html', context)
