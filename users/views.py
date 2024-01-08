from django.shortcuts import render, redirect


def index(request):
    return render(request, 'users/index.html')

def login(request):
    print("login view")
    return render(request, 'users/login.html')

def check(request):
    print("check view")
    return redirect('/')