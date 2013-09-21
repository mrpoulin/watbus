from django import template

register = template.Library()

@register.filter
def location_type_to_string(loc_num):
    if loc_num == 0:
        return "Terminal"
    elif loc_num == 1:
        return "School"
    elif loc_num == 2:
        return "Commerical"
    else:
        return "Invalid loc_num in filter."

