from django.contrib.auth import get_user_model
from .models import Blog, Post
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.utils.html import strip_tags
from django.conf import settings

User = get_user_model()


def is_subscriber(blog_id, user_id) -> bool:
    blog = Blog.objects.get(pk=blog_id)

    if User.objects.get(pk=user_id) in blog.blog_subscribers.all():

        return True
    return False


def is_read(post_id, user_id) -> bool:
    post = Post.objects.get(pk=post_id)

    if User.objects.get(pk=user_id) in post.viewed.all():
        return True
    return False


def is_author(post_id, user_id):
    post = Post.objects.get(pk=post_id)

    if user_id == post.blog.user_id:
        return True
    return False


@receiver(post_save, sender=Post)
def my_handler(sender, instance, **kwargs):

    link = f"{settings.PROJECT_DOMAIN}/post/{instance.id}/"
    post = Post.objects.get(pk=instance.id)

    template_dict = {"link": link, "blog": post.get_name(), "title": post.title}

    template_dir = "email.html"
    html = render_to_string(template_dir, template_dict)
    plain_message = strip_tags(html)

    subject = f'{template_dict["blog"]} published new post!'
    from_email = settings.EMAIL_HOST_USER

    for receiver in post.blog.blog_subscribers.all():
        to = receiver.email
        send_mail(subject, plain_message, from_email, [to], html_message=html)
