from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from application import views as BlogsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('category/', include('application.urls')),
    path('blogs/search/',BlogsViews.search, name='search'),
    path('blogs/<slug:slug>/',BlogsViews.blogs, name='blogs'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', include('dashboard.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
  