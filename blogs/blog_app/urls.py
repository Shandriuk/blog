from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import BlogList, LoginView, LogoutView, Subscribe, Unsubscribe, PostList, MyPostList, Read, PostCreate
from .views import PostDetailView, BlogUpdateView, PostUpdateView, PostDeleteView, BlogDetailView
from django.views.generic import RedirectView


app_name = 'blog_app'

urlpatterns = [
    path('', RedirectView.as_view(permanent=False, url='/myfeed/')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('blogs/', BlogList.as_view(), name="blogs"),
    path('blogs/<int:pk>/subscribe/',  Subscribe.as_view(), name="subscribe"),
    path('blogs/<int:pk>/unsubscribe/', Unsubscribe.as_view(), name="unsubscribe"),
    path('blogs/<int:pk>/blogedit/', BlogUpdateView.as_view(), name="blogedit"),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name="blog"),

    path('myfeed/', PostList.as_view(), name="myfeed"),
    path('post/<int:pk>/read/', Read.as_view(), name="read"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="detail"),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name="postedit"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="postdelete"),
    path('myposts/', MyPostList.as_view(), name="myposts"),


    path('createpost/', PostCreate.as_view(), name="createpost"),

]
