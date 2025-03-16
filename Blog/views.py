from django.shortcuts import render, redirect
from application.models import Category,Blogs
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth,messages
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_feacherd=True, status = 'published')
    posts = Blogs.objects.filter(is_feacherd = False, status = 'published')
    #print(post)

    context = {
        'categories' : categories,
        'featured_post' : featured_post,
        'posts' : posts
    }
    return render(request, 'home.html', context)

# Register form
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context={
       'form':form
    }
    return render(request, 'register.html', context)

# Login form
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Redirect staff and superusers to dashboard, normal users to home
                if user.is_staff or user.is_superuser:
                    return redirect('dashboard')
                return redirect('home')  # Change 'home' to your home page URL name

    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)


# Logout function
def logout(request):
    auth.logout(request)
    return redirect('home')
