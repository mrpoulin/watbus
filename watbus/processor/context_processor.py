'''Thanks to: https://code.djangoproject.com/ticket/18584#no2 for the code!'''
def resolve_urlname(request):
    from django.core.urlresolvers import resolve
    try:
        r = resolve(request.path)

        if r:
            return {'urlname' : r.url_name}

    except:
        return {}
