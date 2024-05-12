from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone number']
        password = request.POST['password']
        customer = User.objects.create_user(username=username,email=email,password=password)
        customer.phone_number = phone
        customer.save()
        login(request, user=customer)
        return redirect('Baby_app:index')

    return render(request, 'users/register.html')

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
    logout(request)
    return redirect('Baby_app:index')