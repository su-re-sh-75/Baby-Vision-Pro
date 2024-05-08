from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('Baby_app:index')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('Baby_app:index')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ('Error while trying to log in'))
            return redirect('users:login')
    else:
        return render(request, 'users/login.html')
        

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Baby_app:index')