from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from watbus import views

urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='/watbus/map')),
        url(r'^search/', views.search, name='search'),
        url(r'^map/$', views.map, name='map'),
        url(r'^browse/$', views.browse, name='browse'),
        url(r'^browse/stops/(?P<stop_id>.+)/$', views.browse_stops, name='browse_stops'),
        url(r'^browse/trips/(?P<trip_id>.+)/$', views.browse_trips, name='browse_trips'),
        url(r'^browse/terminals/$', views.browse_all_terminals, name='browse_all_terminals'),
        url(r'^browse/terminals/(?P<terminal_id>place_.+)/$', views.browse_terminal, name='browse_terminal'),
        url(r'^stopjson$', views.stopjson, name='stopjson')
)
