from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Blog, Post
User = get_user_model()


def is_subscriber(blog_id, user_id) -> bool:
    blog = Blog.objects.get(pk=blog_id)

    if User.objects.get(pk=user_id) in blog.blog_subscribers.all():

        return True
    return False

def is_read(blog_id, user_id) -> bool:
    blog = Post.objects.get(pk=blog_id)

    if User.objects.get(pk=user_id) in blog.viewed.all():
        return True
    return False
