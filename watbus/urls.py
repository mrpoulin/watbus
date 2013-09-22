from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from watbus import views

urlpatterns = patterns('',
        url(r'^$', views.coming, name='comingsoon'),
        url(r'^search/', views.search, name='search'),
        url(r'^map/$', views.map, name='map'),
        url(r'^browse/stops/(?P<stop_id>.+)/$', views.browse_stops, name='browse'),
        url(r'^browse/trips/(?P<trip_id>.+)/$', views.browse_trips, name='browse'),
        url(r'^browse/popular/$', views.popular, name='popular'),
        url(r'^browse/popular_stop/(?P<stop_id>place_.+)/$', views.popular_stop, name='popular'),
        url(r'^stopjson$', views.stopjson, name='stopjson'),
        url(r'^about$', views.about, name='about'),
        url(r'^sitemap$', views.sitemap, name='sitemap')
)
