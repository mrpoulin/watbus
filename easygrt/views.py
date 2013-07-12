from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from datetime import date, time, datetime
from easygrt.models import StopTimes
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
    return render(request, 'easygrt/index.html')

def search(request):

    if 'query' in request.GET and request.GET['query']:
        query = request.GET['query'].strip()
        if not re.match(r'\d+', query):
            return HttpResponseBadRequest("Stop id must only contain numbers")
        return redirect('easygrt.views.browse_stops', stop_id=query)
    else:
        return HttpResponseBadRequest("No query entered")

def map(request):
    return render(request, 'easygrt/map.html')

#Display generic landing page.
def browse(request):
    return render(request, 'easygrt/browse.html')

def browse_stops(request, stop_id):

    curr_time = datetime.time(datetime.now())
    curr_day = date.today()
    day_selector_keyword = 'trip_id__service_id__' + __getWeekdayString(datetime.today().weekday())

    next_buses = StopTimes.objects.filter(stop_id=stop_id)
    if not next_buses:
        raise Http404

    next_buses = next_buses.select_related(
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

    context = { 'next_buses' : next_buses, 'stop_id' : stop_id }
    return render(request, 'easygrt/browse_stops.html', context)

def browse_routes(request, route_id):

    return render(request, 'easygrt/browse_routes.html')

