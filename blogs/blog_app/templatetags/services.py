from ..models import Post, Blog
from ..services import is_subscriber
from django import template

register = template.Library()

@register.simple_tag
def subscriber(blog_id, user):

    if is_subscriber(blog_id, user):
        return 1
    else:
        return 0