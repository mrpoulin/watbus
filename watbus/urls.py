from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from watbus import views

urlpatterns = patterns('',
        url(r'^$', views.coming, name='comingsoon'),
        url(r'^search/', views.search, name='search'),
        url(r'^map/$', views.map, name='map'),
        url(r'^browse/$', views.browse, name='browse'),
        url(r'^browse/stops/(?P<stop_id>.+)/$', views.browse_stops, name='browse'),
        url(r'^browse/trips/(?P<trip_id>.+)/$', views.browse_trips, name='browse'),
        url(r'^browse/terminals/$', views.browse_all_terminals, name='terminals'),
        url(r'^browse/terminals/(?P<terminal_id>place_.+)/$', views.browse_terminal, name='terminals'),
        url(r'^stopjson$', views.stopjson, name='stopjson'),
        url(r'^about$', views.about, name='about'),
        url(r'^sitemap$', views.sitemap, name='sitemap')
)
