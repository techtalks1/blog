from django.shortcuts import render,redirect
from application.models import Category,Blogs
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CategoryForm,BlogPostForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .forms import AddUserForm,EditUserForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# This function checks if the user is staff or superuser.
# If they are not, they cannot access the dashboard.
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='login')

def dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied  # Show 403 Forbidden page
    
    category_counts = Category.objects.all().count()
    blogs_counts = Blogs.objects.all().count()

    context={
       'category_counts':category_counts,
       'blogs_count':blogs_counts,
    }
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html')


def add_categories(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_categories.html', context )

def edit_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method=="POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance= category)
    context = {
        'form':form,
        'category':category
    }
    return render(request, 'dashboard/edit_categories.html', context)

def delete_categories(request,pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blogs.objects.all()
    context={
        'posts':posts
    }
    return render(request, 'dashboard/posts.html',context)

def add_posts(request):
    if request.method=="POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            print("Success")
            return redirect('posts')
        else:
            print(form.errors)
    
    form =BlogPostForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_posts.html',context)

def blog_detail(request, slug):
    post = get_object_or_404(Blogs, slug=slug)
    return render(request, 'dashboard/blog_detail.html', {'post': post})

@login_required
@staff_member_required
def edit_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)  # Fetch the blog post
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)  # Bind form to existing post
        if form.is_valid():
            post = form.save(commit=False)
            title = form.cleaned_data['title']
            post.slug = slugify(title)  # Update the slug
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect('posts')
        else:
            messages.error(request, "Error updating post. Please check the form.")
    else:
        form = BlogPostForm(instance=post)  # Pre-fill form with existing data 

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/edit_post.html', context)

@login_required
@staff_member_required
def delete_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('posts')

def users(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request, 'dashboard/users.html', context)

def add_users(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Hash password
            user.save()
            return redirect('users')
        else:
            print(form.errors) 
    form = AddUserForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_users.html', context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance = user)
    context = {
        'form':form,
        'user':user,
    }
    return render(request, 'dashboard/edit_user.html', context)

def delete_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')



    
