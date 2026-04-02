from django import template
register = template.Library()

@register.filter
def to_cardinal(degree):
    try:
        degree = float(degree)
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                      "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return directions[int((degree / 22.5) + 0.5) % 16]
    except (ValueError, TypeError):
        return ""