from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from easygrt import views

urlpatterns = patterns('',
        url(r'^$', RedirectView.as_view(url='/easygrt/favourites/')),
        url(r'^search/', views.search, name='search'),
        url(r'^favourites/$', views.favourites, name='favourites'),
        url(r'^map/$', views.map, name='map'),
        url(r'^browse/$', views.browse, name='browse'),
        url(r'^browse/stops/(?P<stop_id>\d+)/$', views.browse_stops, name='browse_stops'),
        url(r'^browse/trips/(?P<trip_id>\d+)/$', views.browse_trips, name='browse_trips'),
)
