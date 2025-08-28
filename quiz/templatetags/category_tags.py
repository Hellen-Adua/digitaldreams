# quiz/templatetags/category_tags.py
from django import template

register = template.Library()

@register.inclusion_tag("categories/category_node.html")
def render_category(category, id):
    """
    Render a category with its id (for recursive or accordion-style display).
    """
    return {"category": category, "id": id}
