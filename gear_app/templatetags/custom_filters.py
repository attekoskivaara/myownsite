from django import template
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve an item from a dictionary by key."""
    try:
        return dictionary.get(key, "")
    except (KeyError, TypeError):
        return ""