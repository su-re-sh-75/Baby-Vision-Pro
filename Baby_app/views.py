from django.shortcuts import render

def index(request):
    return render(request, 'Baby_app/index.html')

def about(request):
    pass

def contact(request):
    pass

def login(request):
    pass

def register(request):
    pass

def dashboard(request):
    if request.method == 'POST':
        temp = request.POST['temp']
        msg = request.POST['msg']
    return render(request, 'Baby_app/dashboard.html')