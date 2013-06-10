from django.core.management.base import BaseCommand, CommandError
import os, os.path
from easygrt.adaptors.csv_adaptors import *

class Command(BaseCommand):


    help = "Supply path to data files as only argument"
    
    def handle(self, *args, **options):
        
        if not args or not os.path.exists(args[0]) or not os.path.isdir(args[0]):
            print "Path supplied does not exist or is not a directory."
            return

        base_path = args[0]

        CalendarAdaptor.import_data(data=open(os.path.join(base_path,"calendar.txt")))
        CalendarDatesAdaptor.import_data(data=open(os.path.join(base_path, "calendar_dates.txt")))
        RoutesAdaptor.import_data(data=open(os.path.join(base_path, "routes.txt")))
        StopsAdaptor.import_data(data=open(os.path.join(base_path, "stops.txt")))
        TripsAdaptor.import_data(data=open(os.path.join(base_path, "trips.txt")))
        StopTimes.import_data(data=open(os.path.join(base_path, "stop_times.txt")))
