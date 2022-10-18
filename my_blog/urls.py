"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bloggings import views
from django.contrib.auth.models import User
# from bloggings.views import PostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('my_posts/', views.my_posts, name="my-posts"),
    path('sign-in/', views.connexion, name="connexion"),
    path('logout/', views.logout_view, name="logout"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('home/add', views.addPost, name="add-post"),
    path('home/<int:post_id>/', views.DetailPost, name="details"),
    path('home/<int:post_id>/delete', views.post_delete, name="post-delete"),
    path('home/<int:post_id>/update/', views.post_update, name="post-update"),
    # path('home/<int:post_id>/', views.Commenting, name="commenting"),
]
