from django import template

register = template.Library()

@register.filter
def format_rel_time(reltime):
    if reltime['occurred'] == 1:
        return 'left'

    ret_string = ""
    if reltime['hours'] > 0:
        ret_string = str(reltime['hours']) + " h & "

    ret_string += str(reltime['minutes']) + " m."
    return ret_string
