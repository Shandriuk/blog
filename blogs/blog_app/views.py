from django.shortcuts import render, reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View, CreateView, UpdateView, DetailView, DeleteView
from .models import Blog, Post
from .services import *
from .forms import PostForm
from django.db.models import Q
from django.core.exceptions import PermissionDenied

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
                return HttpResponseRedirect(reverse("blog_app:myfeed"))
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(reverse("blog_app:myfeed"))



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("blog_app:blogs"))


class BlogList(ListView):
    model = Blog
    paginate_by = 10
    template_name = 'blog_app/blogs_list.html'
    def get_queryset(self):

        return Blog.objects.filter(~Q(user=self.request.user.id)).order_by('user')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_app/blog_detail.html'

    def get_context_data(self,  **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context["post_list"] = Post.objects.filter(blog_id=self.kwargs['pk'])
        return context


class Subscribe(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            blog = Blog.objects.get(pk=pk)
            if blog.user != request.user:
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
    paginate_by = 10
    def get_queryset(self):

        return Post.objects.filter(blog__blog_subscribers__id=self.request.user.id).order_by("-create_time")


class Read(View):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            if post.blog.user != request.user:
                post.viewed.add(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse("blog_app:myfeed"))


class MyPostList(ListView):
    template_name = 'blog_app/my_posts.html'
    paginate_by = 10
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
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
    success_url = "/myposts/"

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        form.instance.blog = Blog.objects.get(user=self.request.user)
        return super(PostCreate, self).form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/detail.html'
    def get_context_data(self,  **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(user__id=self.request.user.id)
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        return context

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog_app/post_edit.html'
    fields = ['title', 'text']
    success_url = "/myposts/"

    def get_object(self, *args, **kwargs):
        obj = super(PostUpdateView, self).get_object(*args, **kwargs)
        if not obj.blog.user == self.request.user:
            raise PermissionDenied
        return obj

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog_app/post_delete.html'
    success_url = "/myposts/"

    def get_object(self, *args, **kwargs):
        obj = super(PostDeleteView, self).get_object(*args, **kwargs)
        if not obj.blog.user == self.request.user:
            raise PermissionDenied
        return obj

class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog_app/blog_edit.html'
    fields = ['description']
    success_url = "/myposts/"

    def get_object(self, *args, **kwargs):
        obj = super(BlogUpdateView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj