from django import template

from network.models import Post

register = template.Library()


@register.simple_tag
def is_like(user, arg2=Post):
    if arg2.likes.filter(id=user.id):
        return True
    else:
        return False
