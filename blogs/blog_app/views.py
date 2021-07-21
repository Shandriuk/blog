from django.shortcuts import render, reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View, CreateView, UpdateView
from .models import Blog, Post
from .services import *
from .forms import PostForm
from django.db.models import Q


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
    def get_queryset(self):

        return Blog.objects.filter(~Q(user=self.request.user.id)).order_by('user')


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
            user = User.objects.get(pk=request.user.id)
            blog.blog_subscribers.remove(user)
            posts = Post.objects.filter(blog_id=pk, viewed__id=request.user.id)
            if posts:
                for elem in posts:
                    elem.viewed.remove(user)

            return HttpResponseRedirect(reverse("blog_app:blogs"))


class PostList(ListView):
    template_name = 'blog_app/posts_list.html'

    def get_queryset(self):

        return Post.objects.filter(blog__blog_subscribers__id=self.request.user.id).order_by("-create_time")


class Read(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            post.viewed.add(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse("blog_app:myfeed"))


class MyPostList(ListView):
    template_name = 'blog_app/my_posts.html'

    def get_queryset(self):

        return Post.objects.filter(blog__user__id=self.request.user.id).order_by("-create_time")

    def get_context_data(self,  **kwargs):
        context = super(MyPostList, self).get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(user__id=self.request.user.id)
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog_app/create_post.html'
    context = {'form': form_class}


    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(user=self.request.user)
        return super(PostCreate, self).form_valid(form)

