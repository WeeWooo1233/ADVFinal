from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from .models import List
from .forms import ListForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # Added UserCreationForm import


# Home page (requires login)
@login_required
def home(request):
    query = request.GET.get('q', '')  # Retrieve search query
    if request.method == "POST":
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to reload items after saving
    else:
        if query:
            all_items = List.objects.filter(item__icontains=query)  # Filter items based on query
        else:
            all_items = List.objects.all()  # Show all items if no query
    return render(request, 'home.html', {'all_items': all_items, 'query': query})


# About page (public access)
def about(request):
    return render(request, 'about.html', {})


# Delete item (requires login)
@login_required
def delete(request, item_id):
    item = List.objects.get(pk=item_id)
    item.delete()
    return redirect('home')


# Mark item as completed (requires login)
@login_required
def cross_off(request, item_id):
    item = List.objects.get(pk=item_id)
    item.completed = True
    item.save()
    return redirect('home')


# Unmark item as completed (requires login)
@login_required
def uncross(request, item_id):
    item = List.objects.get(pk=item_id)
    item.completed = False
    item.save()
    return redirect('home')


# Edit item (requires login)
@login_required
def edit(request, item_id):
    item = List.objects.get(pk=item_id)
    if request.method == "POST":
        form = ListForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ListForm(instance=item)
    return render(request, 'edit.html', {'form': form, 'item': item})


# Login view
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})
