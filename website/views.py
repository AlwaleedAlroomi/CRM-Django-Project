from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
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
        records = Record.objects.filter(owner=request.user.id)
        return render(request, template_name='home.html', context={'records':records, 'user':request.user}) # user context to show user name on the screen

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
            messages.error(request, f'{form.errors}')
            form = SignUpForm()       
            return render(request, template_name='register.html', context={'form':form})
    else:
        form = SignUpForm()       
        return render(request, template_name='register.html', context={'form':form})


def person_record(request, pk):
    if request.user.is_authenticated:
        # look up the record
        person_record = Record.objects.get(id=pk)
        if request.user.id == person_record.owner.id:
            return render(request, template_name='record.html', context={'person_record':person_record})
        else:
            messages.error(request, 'You do not have the permission to this record')
            return redirect('home')
    else:
        messages.error(request, "Make sure you are logged in")
        return redirect('home')

def delete(request, pk):
    record = Record.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.user.id == record.owner.id: 
            record.delete()
            messages.success(request, "Recored Deleted successfuly")
            return redirect('home')
        else:
            messages.error(request, 'You do not have the permission to delete this item')
            return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    data = request.POST
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = Record.objects.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    phone = data['phone'],
                    email = data['email'],
                    owner = request.user
                )
                messages.success(request, "Recored Added successfuly")
                return redirect('home')
            else:
                messages.error(request, f'{form.errors}')
                return render(request, template_name='add_record.html', context={'form':form})   
        else:
            return render(request, template_name='add_record.html', context={'form':form})
    else:
        messages.error(request, "Login to be able to add record")
        return redirect('home')        

def edit_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        if request.user.id == current_record.owner.id: 
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been updated")
                return redirect('home')
            else:
                messages.error(request, f'{form.errors}')
                return render(request, template_name='edit_record.html', context={'form':form})
        else:
            messages.error(request, "You do not have the permission to edit this record")
            return redirect('home')
    else:
        messages.error(request, "Login to be able to add record")
        return redirect('home')