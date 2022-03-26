from django import template

register = template.Library()

@register.simple_tag
def isLiked(post, user):
    return post.isLiked(user)

@register.simple_tag
def getLikes(post):
    return post.getLikes()