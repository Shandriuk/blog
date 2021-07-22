from ..models import Post, Blog
from ..services import is_subscriber, is_read, is_author
from django import template

register = template.Library()

@register.simple_tag
def subscriber(blog_id, user):

    if is_subscriber(blog_id, user):
        return 1
    else:
        return 0

@register.simple_tag
def viewed(post_id, user):

    if is_read(post_id, user):
        return 1
    else:
        return 0

@register.simple_tag
def author(post_id, user):

    if is_author(post_id, user):
        return 1
    else:
        return 0