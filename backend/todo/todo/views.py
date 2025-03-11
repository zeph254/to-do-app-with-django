from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from todo.models import TODOO
from . import models
from django.contrib.auth.decorators import login_required # ✅ Correct import
from django.contrib.auth import authenticate, login, logout



def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/login')

    return render(request,'signup.html')

def login_view(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm, pwd)
        user = authenticate(username=fnm, password=pwd)
        if user is not None:
            login(request, user)  # ✅ Now correctly refers to Django's login() function
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request, 'login.html')

@login_required(login_url='/login/')

def todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        print(title)  # Debugging: Check if the title is being received
        
        obj = TODOO(title=title, user=request.user)
        obj.save()
        
        return redirect('/todopage')  # Redirects after saving

    # Correct the field name (assuming 'date' exists instead of 'data')
    res = TODOO.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'todo.html', {'res': res})
    

    # return render(request, 'todo.html')

def edit_todo(request, srno):   
    obj = get_object_or_404(TODOO, srno=srno)  # Fetch object safely

    if request.method == "POST":
        title = request.POST.get("title")
        print(title)  # Debugging: Check if the title is being received
        
        obj.title = title
        obj.save()
        
        return redirect('/todopage')  # Redirects after saving

    res = TODOO.objects.filter(user=request.user).order_by('-date')  # Fetch existing todos
    
    return render(request, 'todo.html', {'res': res, 'todo': obj})  # Pass 'todo' for editing

def signout(request):
    logout(request)
    return redirect('/login/')

def delete_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno)  # Fetch object safely
    obj.delete()
    return redirect('/todopage')  # Redirects after deleting
# Compare this snippet from backend/todo/todo/models.py:
# from django.db import models

