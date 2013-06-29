from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from easygrt import views

urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='/easygrt/favourites/')),
        url(r'^favourites/$', views.favourites, name='favourites'),
        url(r'^map/$', views.map, name='map'),
        url(r'^browse/$', views.browse, name='browse'),
)
