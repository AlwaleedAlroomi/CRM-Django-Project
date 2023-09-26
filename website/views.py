from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
# Create your views here.

def home(request):
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"{username} logged in successfuly")
            return redirect('home')
        else:
            messages.error(request, "There was an error try again")
            return redirect('home')
    else:
        return render(request, template_name='home.html', context={})

def logout_user(request):
    logout(request)
    messages.success(request, "You loggout successfuly")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Auth and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"{username} registered successfuly")
            return redirect('home')
    else:
        form = SignUpForm()       
        return render(request, template_name='register.html', context={'form':form})
