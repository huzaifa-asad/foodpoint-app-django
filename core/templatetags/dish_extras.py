from django import template
from django.templatetags.static import static

register = template.Library()

# Map dish names to static image paths
NAME_TO_STATIC = {
    "Paneer Tikka": "core/images/Paneer Tikka.png",
    "Butter Paneer": "core/images/Butter Paneer.png",
    "Paneer Masala": "core/images/Paneer Masala.png",
}

@register.simple_tag
def dish_img(dish):
    """Return an image URL for a Dish: prefer uploaded, else mapped static, else default paneer."""
    try:
        if getattr(dish, 'image', None):
            f = dish.image
            if f and hasattr(f, 'url') and f.name:
                return f.url
    except Exception:
        pass
    path = NAME_TO_STATIC.get(getattr(dish, 'name', ''), 'core/images/paneer.png')
    return static(path)
