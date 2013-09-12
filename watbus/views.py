from django.shortcuts import render
from django.core import serializers
from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from collections import defaultdict, OrderedDict
from datetime import date, time, datetime
from watbus.models import StopTimes, Stops
import re

def __getWeekdayString(weekday):

    return {

            0 : 'monday',
            1 : 'tuesday',
            2 : 'wednesday',
            3 : 'thursday',
            4 : 'friday',
            5 : 'saturday',
            6 : 'sunday',

            }.get(weekday, 'monday')

def favourites(request):
    return render(request, 'watbus/index.html')

def search(request):

    if 'query' in request.GET and request.GET['query']:
        query = request.GET['query'].strip()
        if not re.match(r'\d+', query):
            return HttpResponseBadRequest("Stop id must only contain numbers")
        return redirect('watbus.views.browse_stops', stop_id=query)
    else:
        return HttpResponseBadRequest("No query entered")

def stopjson(request):
    bus_stop_list = Stops.objects.all();
    bus_json = serializers.serialize("json", bus_stop_list);
    if not bus_stop_list:
        raise Http404
    context = {'bus_stops': bus_stop_list, 'stop_id': 3700, 'bus_json': bus_json}
    return HttpResponse(bus_json, content_type="application/json")

def map(request):
    return render(request, 'watbus/map.html')

#Display generic landing page.
def browse(request):
    return render(request, 'watbus/browse.html')

def browse_stops(request, stop_id):

    curr_time = datetime.time(datetime.now())
    curr_day = date.today()
    day_selector_keyword = 'trip_id__service_id__' + __getWeekdayString(datetime.today().weekday())

    next_bus_list = StopTimes.objects.filter(stop_id=stop_id)
    if not next_bus_list:
        raise Http404

    next_bus_list = next_bus_list.select_related(
            'trip_id'
    ).filter(
            arrival_time__gte=curr_time
    ).filter(
            trip_id__service_id__start_date__lte=curr_day
    ).filter(
            trip_id__service_id__end_date__gte=curr_day
    ).filter(
            **{ day_selector_keyword : 1 }
    ).order_by(
            'arrival_time'
    )
    
    grouped = OrderedDict()

    for bus in next_bus_list:
        route_id = bus.trip_id.route_id.route_id
        if route_id not in grouped:
            grouped[route_id] = [bus]
        else:
            grouped[route_id].append(bus)

    context = { 'next_buses_by_route' : grouped.iteritems(), 'stop_id' : stop_id }
    return render(request, 'watbus/browse_stops.html', context)

def browse_trips(request, trip_id):

    curr_time = datetime.now();
    curr_day = date.today();
    day_selector_keyword = 'trip_id__service_id__' + __getWeekdayString(datetime.today().weekday())

    next_bus_list = StopTimes.objects.filter(trip_id=trip_id)
    if not next_bus_list:
        raise Http404

    
    next_bus_list = next_bus_list.select_related(
            'trip_id'
    ).filter(
            arrival_time__gte=curr_time
    ).filter(
            trip_id__service_id__start_date__lte=curr_day
    ).filter(
            trip_id__service_id__end_date__gte=curr_day
    ).filter(
            **{ day_selector_keyword : 1}
    ).order_by(
            'stop_sequence'
    )

    context = {'next_buses_by_stop' : next_bus_list, 'trip_id' : trip_id }
    return render(request, 'watbus/browse_trips.html', context)
