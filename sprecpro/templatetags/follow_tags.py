from django import template

register = template.Library()

@register.simple_tag
def isFollowedBy(profile, user):
    return profile.isFollowedBy(user)

@register.simple_tag
def getFollowCount(profile):
    return profile.getFollowCount()

@register.simple_tag
def getFollowingCount(profile):
    return profile.getFollowingCount()