from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import BlogList, LoginView, LogoutView, Subscribe, Unsubscribe, PostList, MyPostList, Read, PostCreate
from .views import BlogUpdate

app_name = 'blog_app'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('blogs/', BlogList.as_view(), name="blogs"),
    path('blogs/<int:pk>/subscribe/',  Subscribe.as_view(), name="subscribe"),
    path('blogs/<int:pk>/unsubscribe/', Unsubscribe.as_view(), name="unsubscribe"),

    path('myfeed/', PostList.as_view(), name="myfeed"),
    path('myfeed/<int:pk>/read/', Read.as_view(), name="read"),

    path('myposts/', MyPostList.as_view(), name="myposts"),
    
    path('createpost/', PostCreate.as_view(), name="createpost"),

]
