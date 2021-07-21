from django.shortcuts import render, reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View
from .models import Blog, Post
from .services import *


class LoginView(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("blog_app:blogs"))
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(reverse("blog_app:blogs"))



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("blog_app:blogs"))


class BlogList(ListView):
    model = Blog
    template_name = 'blog_app/blogs_list.html'

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['blog_list'] = Blog.objects.order_by('user')
        return context


class Subscribe(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            blog = Blog.objects.get(pk=pk)
            blog.blog_subscribers.add(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse("blog_app:blogs"))

class Unsubscribe(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            blog = Blog.objects.get(pk=pk)
            blog.blog_subscribers.remove(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse("blog_app:blogs"))


class PostList(ListView):
    template_name = 'blog_app/posts_list.html'

    def get_queryset(self):

        return Post.objects.filter(blog__blog_subscribers__id=self.request.user.id).order_by("-create_time")

    def get_context(self,  **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context["post_list"] = self.get_queryset

        return context

